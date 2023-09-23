from pathlib import Path
import reactpy

_BUNDLE_PATH = Path(__file__).parent / "reactpy-dnd" / "reactpy_dnd" / "bundle.js"
_WEB_MODULE = reactpy.web.module_from_file(
    # Note that this is the same name from package.json - this must be globally
    # unique since it must share a namespace with all other javascript packages.
    name="reactpy-dnd",
    file=_BUNDLE_PATH,
    # What to temporarily display while the module is being loaded
    fallback="Loading...",
)

# Your module must provide a named export for YourFirstComponent
DraggableItem = reactpy.web.export(_WEB_MODULE, "DraggableItem")
ExampleTarget = reactpy.web.export(_WEB_MODULE, "ExampleTarget")
CustomDndProvider = reactpy.web.export(_WEB_MODULE, "CustomDndProvider")

