from lhotse import CutSet, Fbank, FbankConfig, load_manifest, load_manifest_lazy
from lhotse.dataset import (
    CutConcatenate,
    CutMix,
    DynamicBucketingSampler,
    DynamicCutSampler,
    K2SpeechRecognitionDataset,
    PrecomputedFeatures,
    SimpleCutSampler,
    SpecAugment,
)
from torch.utils.data import DataLoader

cuts = load_manifest_lazy("/home/work_nfs8/xlgeng/new_workspace/icefall/egs/aishell/ASR/gxl_data/fbank_common/gxldata_cuts_test_2.jsonl.gz")
test = K2SpeechRecognitionDataset(
            input_strategy=PrecomputedFeatures(),
            return_cuts=True,
        )
sampler = SimpleCutSampler(
    cuts,
    max_duration=100,
    shuffle=False,
    # num_buckets=1
)
test_dl = DataLoader(
    test,
    batch_size=None,
    sampler=sampler,
    num_workers=8,
)
num = 0
for batch in test_dl:
    """"""
    feature = batch["inputs"]
    # at entry, feature is (N, T, C)
    assert feature.ndim == 3
    supervisions = batch["supervisions"]
    feature_lens = supervisions["num_frames"]
    texts = batch["supervisions"]["text"]
    a = batch["supervisions"]["cut"][0]
    print(a)
    label = a.id
    label = [item.supervisions[0].speaker for item in  batch["supervisions"]["cut"]]
    print(f'{num} {feature.shape}, {feature_lens}, {texts},  {label}')
    num += 1
    if num < 1:
        continue
    else:
        break

