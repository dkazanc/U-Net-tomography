import torch
import torch.nn.functional as F
from tqdm import tqdm


def eval_net(net, loader, device):
    """Evaluation without the densecrf with the dice coefficient"""
    net.eval()
    mask_type = torch.float32 if net.n_classes == 1 else torch.long
    n_val = len(loader)  # the number of batch
    tot = 0

    with tqdm(total=n_val, desc='Validation round', unit='batch', leave=False) as pbar:
        for batch in loader:
            imgs, true_masks = batch['image'], batch['mask']
            imgs = imgs.to(device=device, dtype=torch.float32)
            true_masks = true_masks.to(device=device, dtype=mask_type)

            with torch.no_grad():
                mask_pred = net(imgs)
            
            true_masks = true_masks.squeeze(1)
            tot += F.cross_entropy(mask_pred, true_masks).item() #?! .squeeze(0)
            pbar.update()

    net.train()
    return tot / n_val
