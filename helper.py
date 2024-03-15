from matplotlib import pyplot as plt


def visualize_predictions(imgs, pred, i):

    if i > 8:
        return

    print(imgs.shape)
    imgs = imgs.detach().cpu().numpy()

    print(type(imgs))
    print(pred[0].shape)
    print(pred)
    print(i)
    #exit(-1)

    for i, pi in enumerate(p):  # layer index, layer predictions
        b, a, gj, gi = indices[i]  # image, anchor, gridy, gridx
        

        n = b.shape[0]  # number of targets
        if n:
            # pxy, pwh, _, pcls = pi[b, a, gj, gi].tensor_split((2, 4, 5), dim=1)  # faster, requires torch 1.8.0
            pxy, pwh, _, pcls = pi[b, a, gj, gi].split((2, 2, 1, self.nc), 1)  # target-subset of predictions

            # Regression
            pxy = pxy.sigmoid() * 2 - 0.5
            pwh = (pwh.sigmoid() * 2) ** 2 * anchors[i]
            pbox = torch.cat((pxy, pwh), 1)  # predicted box
            iou = bbox_iou(pbox, tbox[i], CIoU=True).squeeze()  # iou(prediction, target)
            lbox += (1.0 - iou).mean()  # iou loss

            # Objectness
            iou = iou.detach().clamp(0).type(tobj.dtype)
            if self.sort_obj_iou:
                j = iou.argsort()
                b, a, gj, gi, iou = b[j], a[j], gj[j], gi[j], iou[j]
            if self.gr < 1:
                iou = (1.0 - self.gr) + self.gr * iou
            tobj[b, a, gj, gi] = iou  # iou ratio

            # Classification
            if self.nc > 1:  # cls loss (only if multiple classes)
                t = torch.full_like(pcls, self.cn, device=self.device)  # targets
                t[range(n), tcls[i]] = self.cp
                lcls += self.BCEcls(pcls, t)  # BCE

            # Append targets to text file
            # with open('targets.txt', 'a') as file:
            #     [file.write('%11.5g ' * 4 % tuple(x) + '\n') for x in torch.cat((txy[i], twh[i]), 1)]

        obji = self.BCEobj(pi[..., 4], tobj)
        lobj += obji * self.balance[i]  # obj loss
        if self.autobalance:
            self.balance[i] = self.balance[i] * 0.9999 + 0.0001 / obji.detach().item()

        if self.autobalance:
            self.balance = [x / self.balance[self.ssi] for x in self.balance]
        lbox *= self.hyp["box"]
        lobj *= self.hyp["obj"]
        lcls *= self.hyp["cls"]
        bs = tobj.shape[0]  # batch size
    