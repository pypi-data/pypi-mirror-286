import base64
import json
import os
import requests
import pandas as pd


def encoded(filepath):
    with open(filepath, "rb") as file:
        encoded_content = base64.b64encode(file.read()).decode("utf-8")
    return f"data:application/pdf;base64,{encoded_content}"


def file(filepath, parser_type="tela-pdf-parser", range=None):
    options = {"parserType": parser_type}
    if range is not None:
        options["range"] = range
    return {
        "file_url": encoded(filepath),
        "options": options
    }


class TelaClient:
    def __init__(self, api_key, api_url="https://api.tela.com", max_attempts=3):
        self.api_key = api_key
        self.api_url = api_url
        self.max_attempts = max_attempts

    def request(self, documents, canvas_id, override=None):
        try:
            url = f"{self.api_url}/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            data = {
                "uses": canvas_id,
                "with": documents,
                "input": "",
                "long_response": True,
            }
            if override:
                data["override"] = override
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                print(response.json())
                print(response.status_code)
            return response.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def new_canvas(self, canvas_id, expected_input=None):
        return Canvas(self, canvas_id, expected_input, self.max_attempts)


class Canvas:
    def __init__(self, tela_client, canvas_id, expected_input=None, max_attempts=3):
        self.canvas_id = canvas_id
        self.tela_client = tela_client
        self.expected_input = expected_input
        self.max_attempts = max_attempts

    def run(self, output_type='json',override=None, **kwargs):
        documents = {}
        if self.expected_input:
            for i in self.expected_input:
                if i in kwargs:
                    documents[i] = kwargs[i]
                else:
                    raise ValueError(f"Missing expected input: {i}")
        else:
            documents = kwargs

        attempts = 0
        response = None
        while attempts < self.max_attempts:
            response = self.tela_client.request(documents, self.canvas_id,override)
            if response and "choices" in response and len(response["choices"]) > 0:
                break
            attempts += 1

        if response and "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            if output_type == 'dataframe':
                return self._json_to_dataframe(content)
            return content
        return None

    def run_batch(self, inputs, output_type='json', max_workers=10):
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def process_input(input_data):
            return self.run(output_type=output_type, **input_data)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_input, input_data) for input_data in inputs]
            results = []
            for future in as_completed(futures):
                results.append(future.result())

        return results

    def _json_to_dataframe(self, json_data):
        def flatten_json(data, prefix=''):
            items = {}
            for key, value in data.items():
                new_key = f"{prefix}{key}"
                if isinstance(value, dict):
                    items.update(flatten_json(value, f"{new_key}_"))
                elif isinstance(value, list):
                    items[new_key] = json.dumps(value)
                else:
                    items[new_key] = value
            return items

        def process_json(data):
            if isinstance(data, dict):
                return [flatten_json(data)]
            elif isinstance(data, list):
                return [flatten_json(item) if isinstance(item, dict) else item for item in data]

        processed_data = process_json(json_data)
        df = pd.DataFrame(processed_data)

        # Expand columns that contain JSON strings (lists or list of objects)
        for column in df.columns:
            try:
                df[column] = df[column].apply(json.loads)
                if df[column].apply(lambda x: isinstance(x, list)).all():
                    if isinstance(df[column].iloc[0][0], dict):
                        # Handle list of objects
                        expanded_df = pd.json_normalize(df[column].explode().tolist())
                        expanded_df.index = df.index.repeat(df[column].str.len())
                        expanded_df.columns = [f"{column}_{subcol}" for subcol in expanded_df.columns]
                        df = df.drop(columns=[column]).join(expanded_df)
                    else:
                        # Handle simple lists
                        df = df.explode(column)
            except:
                pass

        return df


# EXAMPLE USAGE
# from tela.tela import TelaClient, file

# TELA_API_KEY = "Your API KEY"
# tela_client = TelaClient(TELA_API_KEY)

# canvas_id = "2b57f4ae-c48e-4883-a0a4-130a573ffdfc"
# canvas = tela_client.new_canvas(canvas_id, expected_input=['document'])

# FILE_NAME = "./Cartao CNPJ produtor.pdf"
# canvas.run(document=file(FILE_NAME))