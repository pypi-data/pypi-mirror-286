import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities

class Switch:
    def __init__(self):
        # self.functionApply = ["is null", "is not null", "in", "not in"]
        # self.noValueRequired = ["is empty", "is not empty"]
        self.noValueRequired = ["is null", "is not null", "is empty", "is not empty", "True", "False", "is_infinity", "is_not_infinity"]

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SWITCH")

        cases: list = settings["cases"] if "cases" in settings and settings["cases"] else []
        default_value: str | None = settings["default_value"] if "default_value" in settings and settings["default_value"] else None
        default_value_field: str | None = settings["default_value_field"] if "default_value_field" in settings and settings["default_value_field"] else None
        new_column: str = settings["new_column"] if "new_column" in settings and settings["new_column"] else "new_column"

        if default_value == None and default_value_field == None:
            msg = app_message.dataprep["nodes"]["switch"]["default_value"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg)

        try:
            conditions = []
            outputs = []
            script.append("conditions = []")
            script.append("outputs = []")
            for caseIdx, case in enumerate(cases):
                output: str = case["output"] if "output" in case else None
                output_field: str = case["output_field"] if "output_field" in case else None
                if not output and not output_field:
                    msg = app_message.dataprep["nodes"]["switch"]["no_return_value"](node_key, caseIdx + 1)
                    return bug_handler.default_node_log(flow_id, node_key, msg)

                query = ""
                case_conditions: list = case["conditions"] if "conditions" in case else []
                if not case_conditions:
                    msg = app_message.dataprep["nodes"]["switch"]["no_conditions"](node_key, caseIdx + 1)
                    return bug_handler.default_node_log(flow_id, node_key, msg)

                for condIdx, condition in enumerate(case_conditions):
                    rule: str = f" {condition['rule']} " if "rule" in condition else ""
                    field: str = condition["field"] if "field" in condition and condition["field"] else None
                    operator: str = condition["operator"] if "operator" in condition and condition["operator"] else None

                    value: str = utilities.check_and_add_flow_vars(flow_id, condition["value"]) if "value" in condition else None
                    value_field: str = condition["value_field"] if "value_field" in condition else None

                    # Validar campos requeridos para la condicion
                    if condIdx > 0 and not rule:
                        msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Rule", caseIdx + 1, condIdx + 1)
                        return bug_handler.default_node_log(flow_id, node_key, msg)

                    if not field:
                        msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Column", caseIdx + 1, condIdx + 1)
                        return bug_handler.default_node_log(flow_id, node_key, msg)

                    if not operator:
                        msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Operator", caseIdx + 1, condIdx + 1)
                        return bug_handler.default_node_log(flow_id, node_key, msg)

                    # * Operaciones que no requieren value
                    if operator in self.noValueRequired:
                        if operator == "is null":
                            value = f"pd.isnull(df['{field}'])"

                        elif operator == "is not null":
                            value = f"pd.notnull(df['{field}'])"

                        elif "empty" in operator:
                            value = f'df["{field}"] == ""' if operator == "is empty" else f'df["{field}"] != ""'

                        elif operator == "is_infinity":
                            value = f"(df['{field}'] == np.inf) | (df['{field}'] == -np.inf)"

                        elif operator == "is_not_infinity":
                            value = f"(df['{field}'] != np.inf) & (df['{field}'] != -np.inf)"

                        # TODO: Revisar casos bools
                        elif operator == "True":
                            value = f"df['{field}'] == True"
                        elif operator == "False":
                            value = f"df['{field}'] == False"

                        query += f"{rule}({value})"

                    # * Operaciones que REQUIEREN value o value_field
                    else:
                        # * Validar value y value_field para los operadores que lo requieren
                        if (value == None or value == "") and (value_field == None or value_field == ""):
                            msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Value", caseIdx + 1, condIdx + 1)
                            return bug_handler.default_node_log(flow_id, node_key, msg)

                        # * si existe value
                        if value != None and value != "":
                            if operator == "in":
                                # TODO: Hay que quitar los astype cuando se solucione el problema en el dtypes al pasar a string
                                df[field] = df[field].astype(str)
                                value = f"df['{field}'].str.contains('{value}')"
                                query += f"{rule}({value})"

                            elif operator == "not in":
                                # TODO: Hay que quitar los astype cuando se solucione el problema en el dtypes al pasar a string
                                df[field] = df[field].astype(str)
                                value = f"~df['{field}'].str.contains('{value}')"
                                query += f"{rule}({value})"

                            else:
                                # ? Agregar comillas si el tipo de la columna es string o datetime
                                value = "'{}'".format(value) if pd.api.types.is_string_dtype(df[field]) or pd.api.types.is_datetime64_any_dtype(df[field]) else value
                                query += f"{rule}(df['{field}'] {operator} {value})"

                        # * si existe value_field
                        else:
                            if not value_field or value_field not in df.columns:
                                msg = app_message.dataprep["nodes"]["switch"]["no_column_in_df"](node_key, value_field)
                                return bug_handler.default_node_log(flow_id, node_key, msg)

                            query += f"{rule}(df['{field}'] {operator} df['{value_field}'])"
                            
                output_new = output if output else df[output_field]
                outputs.append(output_new)
                script.append(f"outputs.append('{output_new}')")
                conditions.append(eval(query))
                script.append(f'conditions.append(pd.eval("{query}"))')

            df[new_column] = np.select(conditions, outputs, default=default_value if default_value else df[default_value_field])

            try:
                df[new_column] = pd.to_numeric(df[new_column])
            except Exception as e:
                print(new_column, e)

            default_value_new = "'" + default_value + "'" if default_value else "df['" + default_value_field + "']"
            script.append(f'df["{new_column}"] = np.select(conditions, outputs, default={default_value_new})')

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
