import tqdm.auto as tqdm

_model = None
_portraits_features = None


def get_feature_vector(model, images, average_multiple: int = 1):
    import torch
    import torchvision.transforms as T

    @torch.no_grad()
    def call_model(im):
        out = model(im.to(device))
        return out.view(im.size(0), -1).cpu()

    def get_features():
        return torch.cat([call_model(o)
                          for o in tqdm.tqdm(dl, total=len(dl))], 0)

    if average_multiple > 1:
        tfm = T.Compose([T.ToPILImage(),
                         T.Resize(256),
                         T.RandomCrop(224),
                         T.GaussianBlur(3),
                         T.ToTensor(),
                         T.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])])
    else:
        tfm = T.Compose([T.ToPILImage(),
                         T.Resize(256),
                         T.CenterCrop(224),
                         T.ToTensor(),
                         T.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])])

    bs = 16
    ds = _OptcBxDataset([o[...,::-1] for o in images], transform=tfm)
    dl = torch.utils.data.DataLoader(ds, batch_size=bs)
    device = list(model.parameters())[0].device

    features = sum(get_features() for _ in range(average_multiple))
    features = features / average_multiple
    return features


def feature_extractor():
    global _model
    import torch
    import torchvision.models as zoo

    if _model is None:
        _model = zoo.resnet18(pretrained=False)
        _model = torch.nn.Sequential(*list(_model.children())[:-1])
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        _model.load_state_dict(torch.load('ai/fe.pt', map_location=device))
        _model.eval()

    return _model


def load_portrait_features():
    global _portraits_features

    if _portraits_features is None:
        import torch
        _portraits_features = torch.load('ai/fv-portraits.pt', 
                                         map_location=torch.device('cpu'))
        _portraits_features.unsqueeze_(0)

    return _portraits_features


class _OptcBxDataset(object):

    def __init__(self, images, transform=None):
        self.images = images
        self.transform = transform

    def __getitem__(self, index):
        x = self.images[index]

        if self.transform is not None:
            x = self.transform(x)

        return x

    def __len__(self):
        return len(self.images)
