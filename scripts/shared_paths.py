from pathlib import Path

from modules import scripts, shared

try:
    from modules.paths import extensions_dir, script_path

    # Webui root path
    FILE_DIR = Path(script_path).absolute()

    # The extension base path
    EXT_PATH = Path(extensions_dir).absolute()
except ImportError:
    # Webui root path
    FILE_DIR = Path().absolute()
    # The extension base path
    EXT_PATH = FILE_DIR.joinpath("extensions").absolute()

# Tags base path
TAGS_PATH = Path(scripts.basedir()).joinpath("tags").absolute()

# Determine the model directory, which may be customized by the user
def get_model_directory():
    try:
        # Attempt to get the custom model directory set by the user
        model_dir = Path(shared.cmd_opts.models_dir).absolute()
    except AttributeError:
        # If no custom model directory is set, use the default 'models' directory in the root
        model_dir = FILE_DIR.joinpath("models").absolute()
    return model_dir

# The path to the folder containing the wildcards, which depends on the model directory
MODEL_DIR = get_model_directory()
WILDCARD_PATH = MODEL_DIR.joinpath("wildcards").absolute()

EMB_PATH = Path(shared.cmd_opts.embeddings_dir).absolute()
HYP_PATH = Path(shared.cmd_opts.hypernetwork_dir).absolute()

try:
    LORA_PATH = Path(shared.cmd_opts.lora_dir).absolute()
except AttributeError:
    LORA_PATH = None

try:
    try:
        LYCO_PATH = Path(shared.cmd_opts.lyco_dir_backcompat).absolute()
    except:
        LYCO_PATH = Path(shared.cmd_opts.lyco_dir).absolute() # attempt original non-backcompat path
except AttributeError:
    LYCO_PATH = None


def find_ext_wildcard_paths():
    """Returns the path to the extension wildcards folder"""
    found = list(EXT_PATH.glob("*/wildcards/"))

    # Adding a specific path for the wildcards folder in your extension
    specific_wildcard_path = MODEL_DIR.joinpath("wildcards")
    if specific_wildcard_path.exists():
        found.insert(0, specific_wildcard_path)  # Ensure this path is searched first

    # Try to find the wildcard path from the shared opts
    try:
        from modules.shared import opts
    except ImportError:  # likely not in an a1111 context
        opts = None

    # Append custom wildcard paths
    custom_paths = [
        getattr(shared.cmd_opts, "wildcards_dir", None),    # Cmd arg from the wildcard extension
        getattr(opts, "wildcard_dir", None),                # Custom path from sd-dynamic-prompts
    ]
    for path in [Path(p).absolute() for p in custom_paths if p is not None]:
        if path.exists():
            found.append(path)

    return found


# The path to the extension wildcards folder
WILDCARD_EXT_PATHS = find_ext_wildcard_paths()

# The path to the temporary files
# In the webui root, on windows it exists by default, on linux it doesn't
STATIC_TEMP_PATH = FILE_DIR.joinpath("tmp").absolute()
TEMP_PATH = TAGS_PATH.joinpath("temp").absolute()  # Extension specific temp files

# Make sure these folders exist
if not TEMP_PATH.exists():
    TEMP_PATH.mkdir()
if not STATIC_TEMP_PATH.exists():
    STATIC_TEMP_PATH.mkdir()
