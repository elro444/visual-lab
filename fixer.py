from reactpy import component, web

mui = web.module_from_template(
    "react@^17.0.0",
    "@material-ui/core@4.12.4",
    fallback="⌛",
)
Button = web.export(mui, "Button")
Tooltip = web.export(mui, "Tooltip")


