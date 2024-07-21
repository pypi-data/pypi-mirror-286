from typing import List
from .write_to_path import write_to_file

def process_templates(config, rendered_templates):
    source_outputs = []

    if isinstance(config.source.outputs, str):
        source_outputs = [config.source.outputs]
    elif isinstance(config.source.outputs, List):
        source_outputs = config.source.outputs

    for o in source_outputs:
        outputs = []

        for conf in config.compose:
            if isinstance(conf, str):
                rendered = rendered_templates[conf]
                if rendered not in outputs:
                    outputs.append(rendered)
                continue

            if "output" in conf and o in conf["output"]:
                outputs.append(rendered_templates[conf["template"]])
                continue

            if "template" in conf and "output" not in conf:
                rendered = rendered_templates[conf["template"]]
                if rendered not in outputs:
                    outputs.append(rendered)

        write_to_file(o, "\n\n".join(outputs))
