import logging

"""Downloading models in advance inside the docker container."""

logger = logging.getLogger(__name__)

"""
These are versions of the models that are used at the current moment - hashes of commits from https://huggingface.co/dedoc.
Keys are the names of repositories with models.
"""
model_hash_dict = dict(
    txtlayer_classifier="9ca1de749d8d37147b00a3a228e03ee1776c695f",
    scan_orientation_efficient_net_b0="c60812552a1be624476c1e5b58599867b36f8d4e",
    font_classifier="db4481ad60ab050cbb42079b64f97f9e431feb07",
    paragraph_classifier="97c4b78bc20d87ec7d53389e09f1ca35c6ade067",
    line_type_classifiers="6ad0eacbfdea065b658cb6f039d13f75245d51ae",
    fintoc_classifiers="6a907b7d2437c3f61ac9c506f67175207982fae8",
    torch_cnn="5333909f858f5f632df478ef5a53af6dfd26f2e1"
)


# region FUNC_download_from_hub [DOMAIN(7): MLModelManagement; CONCEPT(6): ModelDownload; TECH(7): HuggingFaceHub]
## @purpose To download a single model file from HuggingFace Hub by repository name and commit hash, moving it to the specified output directory — serving as the atomic download unit for all Dedoc ML models.
## @uses huggingface_hub.hf_hub_download, model_hash_dict
## @io (str, str, str, str, str) -> None
## @complexity 5
def download_from_hub(out_dir: str, out_name: str, repo_name: str, hub_name: str, user_name: str = "dedoc") -> None:
    import os
    import shutil
    from huggingface_hub import hf_hub_download

    # LDD-log: download start
    logger.info(f"[IMP:7][download_from_hub][DOWNLOAD] Downloading {repo_name}/{hub_name} from {user_name}")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.realpath(hf_hub_download(repo_id=f"{user_name}/{repo_name}", filename=hub_name, revision=model_hash_dict[repo_name]))
    shutil.move(path, os.path.join(out_dir, out_name))
    # LDD-log: download complete
    logger.info(f"[IMP:8][download_from_hub][DOWNLOAD_COMPLETE] Saved {out_name} to {out_dir}")
# endregion FUNC_download_from_hub


# region FUNC_download [DOMAIN(7): MLModelManagement; CONCEPT(7): ModelProvisioning; TECH(7): HuggingFaceHub]
## @purpose To download all ML models required by Dedoc (text layer classifier, scan orientation, font classifier, paragraph classifier, line type classifiers, Fintoc classifiers, torch CNN) into the specified resources directory, ensuring the container is provisioned with all inference assets.
## @uses download_from_hub, model_hash_dict
## @io str -> None
## @complexity 6
def download(resources_path: str) -> None:
    import os

    # LDD-log: batch download start
    logger.info(f"[IMP:7][download][BATCH_START] Downloading all models to {resources_path}")

    download_from_hub(out_dir=resources_path, out_name="txtlayer_classifier.json", repo_name="txtlayer_classifier", hub_name="model.json")

    download_from_hub(out_dir=resources_path,
                      out_name="scan_orientation_efficient_net_b0.pth",
                      repo_name="scan_orientation_efficient_net_b0",
                      hub_name="model.pth")

    download_from_hub(out_dir=resources_path, out_name="paragraph_classifier.zip", repo_name="paragraph_classifier", hub_name="model.zip")

    line_clf_resources_path = os.path.join(resources_path, "line_type_classifiers")
    for classifier_type in ("diploma", "law", "law_txt", "tz", "tz_txt"):
        download_from_hub(out_dir=line_clf_resources_path,
                          out_name=f"{classifier_type}_classifier.zip",
                          repo_name="line_type_classifiers",
                          hub_name=f"{classifier_type}.zip")

    fintoc_classifiers_resources_path = os.path.join(resources_path, "fintoc_classifiers")
    for language in ("en", "fr", "sp"):
        for classifier_type in ("target", "binary"):
            download_from_hub(out_dir=fintoc_classifiers_resources_path,
                              out_name=f"{classifier_type}_classifier_{language}.json",
                              repo_name="fintoc_classifiers",
                              hub_name=f"{classifier_type}_classifier_{language}_txt_layer.json")

    download_from_hub(out_dir=resources_path, out_name="glyph_recognizer.pt", repo_name="torch_cnn", hub_name="rus_eng.pt", user_name="sinkudo")

    # LDD-log: batch download complete
    logger.info(f"[IMP:9][download][BATCH_COMPLETE] All models downloaded to {resources_path}")
# endregion FUNC_download

# region MODULE_CONTRACT [DOMAIN(7): MLModelManagement; CONCEPT(7): ModelProvisioning, DockerSetup; TECH(7): HuggingFaceHub]
## @modulecontract
## @purpose To download and provision all ML inference models (classifiers, orientation detectors, OCR support models) from HuggingFace Hub into the local resources directory, typically executed during Docker image build to pre-cache models before serving.
## @scope Model downloading from HuggingFace Hub, Docker container provisioning, model version management via commit hashes.
## @input Resources directory path.
## @output Downloaded model files (JSON, PTH, ZIP, PT) placed in the resources directory.
## @links [USES_API(9): huggingface_hub.hf_hub_download; READS_DATA_FROM(8): model_hash_dict]
## @invariants
## - All models are downloaded with pinned commit hashes from model_hash_dict for reproducibility.
## - Download failures are not caught — they fail fast during container build.
## @rationale
## Q: Why download models in advance rather than on-demand?
## A: Dedoc serves document processing in a Docker container; downloading multi-GB models at request time would cause unacceptable latency. Pre-provisioning ensures instant availability.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## DATA 10[Model version hashes] => model_hash_dict
## FUNC 9[Downloads single model from HuggingFace] => download_from_hub
## FUNC 10[Downloads all required models] => download
## @usecases
## - [download]: DockerBuilder => ProvisionAllModels => ReadyForInference
## - [download_from_hub]: ModelManager => FetchSpecificModel => ModelFileSaved
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: download models, HuggingFace Hub, model provisioning, Docker, ML classifiers, txtlayer, scan orientation, font classifier, paragraph classifier, line type classifiers, Fintoc, torch CNN, model hash
# STRUCTURE: ▶ download(resources_path) → ⚡ download_from_hub × N → ○ txtlayer_clf | scan_orientation | paragraph_clf | line_type_clfs ⟦loop: diploma,law,law_txt,tz,tz_txt⟧ | fintoc_clfs ⟦loop: en,fr,sp × target,binary⟧ | torch_cnn → ∑ all models cached


if __name__ == "__main__":
    from dedoc.config import get_config

    resources_path = get_config()["resources_path"]
    download(resources_path)
