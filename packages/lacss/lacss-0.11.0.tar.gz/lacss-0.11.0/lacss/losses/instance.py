from __future__ import annotations

from functools import partial

import jax
import jax.numpy as jnp
import optax

from xtrain import unpack_x_y_sample_weight

from ..ops import sub_pixel_samples, gather_patches
from ..ops.patches import _get_patch_data

from .common import binary_focal_factor_loss, mean_over_boolean_mask, sum_over_boolean_mask

def supervised_instance_loss(batch, prediction):
    """LACSS instance loss, supervised with segmentation label"""
    preds = prediction["predictions"]
    _, labels, _ = unpack_x_y_sample_weight(batch)

    if labels is None:
        return None

    instance_mask = preds["segmentation_is_valid"]
    instance_logit = preds["segmentations"]

    n_patches = instance_logit.shape[0]
    patch_size = instance_logit.shape[-1]

    if not isinstance(labels, dict):
        labels = dict(gt_labels=labels)

    if "gt_labels" in labels:  # labeled with image label
        gt_labels = labels["gt_labels"].astype("int32")
        y0 = preds["segmentation_y0_coord"]
        x0 = preds["segmentation_x0_coord"]

        if gt_labels.ndim == 2:
            gt_labels = gt_labels[None, :, :]

        gt_patches = jax.vmap(
            lambda x: gather_patches(x, jnp.stack([y0, x0], axis=-1), patch_size),
        )(gt_labels)

        gt_patches = gt_patches == jnp.arange(1, n_patches+1)[:, None, None]

        gt_patches = gt_patches.swapaxes(0, 1) # back to [N, D, PS, PS]

        gt_patches = gt_patches.astype("float32")

    else: # only works for 2d input
        assert instance_logit.shape[1] == 1

        gt_segs = labels["gt_masks"]
        if len(gt_segs.shape) == 4:  # either NxHxWx1 or NxHxW
            gt_segs = gt_segs.squeeze(-1)
        seg_size = gt_segs.shape[1]

        assert gt_segs.shape[0] == n_patches

        # pixel size of the gt mask labels
        y0, x0, y1, x1 = jnp.swapaxes(labels["gt_bboxes"], 0, 1)
        hs = (y1 - y0) / seg_size
        ws = (x1 - x0) / seg_size

        # compute rescaled coorinats in edge indexing
        yc, xc = jnp.mgrid[:patch_size, :patch_size]
        yc = yc + preds["segmentation_y0_coord"][:, None, None]
        xc = xc + preds["segmentation_x0_coord"][:, None, None]
        yc = (yc - y0[:, None, None] + 0.5) / hs[:, None, None]
        xc = (xc - x0[:, None, None] + 0.5) / ws[:, None, None]

        # resample the label to match model coordinates
        gt_patches = jax.vmap(sub_pixel_samples)(
            gt_segs,
            jnp.stack([yc, xc], axis=-1) -.5,
        )

        gt_patches = gt_patches[:, None, :, :] # [N, 1, PS, PS]

        gt_patches = (gt_patches >= 0.5).astype("float32")

    loss = optax.sigmoid_binary_cross_entropy(instance_logit, gt_patches)

    return mean_over_boolean_mask(loss, instance_mask)

def self_supervised_instance_loss(batch, prediction, *, soft_label: bool = True):
    """Unsupervised instance loss"""
    preds = prediction["predictions"]

    instance_mask = preds["segmentation_is_valid"]
    instance_logit, yc, xc = _get_patch_data(preds)
    instances = jax.nn.sigmoid(instance_logit)

    # instance_logit = preds["segmentations"]
    # yc = preds["segmentation_y_coords"]
    # xc = preds["segmentation_x_coords"]

    patch_size = instances.shape[-1]
    padding_size = patch_size // 2 + 2
    yc += padding_size
    xc += padding_size

    binary_mask = jax.lax.stop_gradient(jax.nn.sigmoid(preds["fg_pred"]))
    seg = jnp.pad(binary_mask, padding_size)

    if soft_label:
        seg_patch = seg[yc, xc]

        loss = (1 - seg_patch) * instances + seg_patch * (1 - instances)

        instance_sum = jnp.zeros_like(seg)
        instance_sum = instance_sum.at[yc, xc].add(instances)
        instance_sum_i = instance_sum[yc, xc] - instances

        loss += instances * instance_sum_i

    else:
        seg = (seg > 0.5).astype(instances.dtype)
        seg_patch = seg[yc, xc]

        loss = (1 - seg_patch) * instances + seg_patch * (1 - instances)

        log_yi_sum = jnp.zeros_like(seg)
        log_yi = -jax.nn.log_sigmoid(-instance_logit)
        log_yi_sum = log_yi_sum.at[yc, xc].add(log_yi)
        log_yi = log_yi_sum[yc, xc] - log_yi

        loss = loss + (instances * log_yi)

    return mean_over_boolean_mask(loss, instance_mask)


def weakly_supervised_instance_loss(batch, prediction, *, ignore_mask: bool = False):
    """Instance loss supervised by image mask instead of instance masks"""
    preds = prediction["predictions"]
    inputs, labels, _ = unpack_x_y_sample_weight(batch)

    instance_mask = preds["segmentation_is_valid"]
    instance_logit, yc, xc = _get_patch_data(preds)
    instances = jax.nn.sigmoid(instance_logit)
    log_yi = -jax.nn.log_sigmoid(-instance_logit)

    patch_size = instances.shape[-1]
    padding_size = patch_size // 2 + 2
    yc += padding_size
    xc += padding_size

    # dealing with masked out entries
    if ignore_mask:
        seg = jnp.zeros(inputs["image"].shape[:-1])
        seg = jnp.pad(seg, padding_size)
        loss = jnp.zeros_like(instances)
    else:
        if isinstance(labels, dict):
            seg = labels["gt_image_mask"].astype("float32")
        else:
            seg = labels.astype("float32")
        seg = jnp.pad(seg, padding_size)
        seg_patch = seg[yc, xc]
        loss = (1.0 - seg_patch) * instances + seg_patch * (1.0 - instances)

    log_yi_sum = jnp.zeros_like(seg, dtype="float32")
    log_yi_sum = log_yi_sum.at[yc, xc].add(log_yi)
    log_yi_inv = log_yi_sum[yc, xc] - log_yi

    loss = loss + (instances * log_yi_inv)
    loss = loss.mean(axis=(1,2))
    assert loss.ndim == 1

    return mean_over_boolean_mask(loss, instance_mask)


def segmentation_loss(batch, prediction, *, pretraining=False):
    _, labels, _ = unpack_x_y_sample_weight(batch)

    if labels is None:
        labels = {}

    if "gt_labels" in labels or "gt_masks" in labels:  # supervised
        return supervised_instance_loss(batch, prediction)
    elif "gt_image_mask" in labels:  # supervised by point + imagemask
        return weakly_supervised_instance_loss(batch, prediction)
    else:  # point-supervised
        return self_supervised_instance_loss(
            batch, prediction, soft_label=not pretraining
        )
