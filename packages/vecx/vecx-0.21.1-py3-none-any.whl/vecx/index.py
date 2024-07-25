import requests, json
from .libvx import encode, decode, encode_vector
from .crypto import encrypt_ecb, decrypt_ecb, get_checksum
from .exceptions import raise_exception

class Index:
    def __init__(self, name:str, key:str, token:str, lib_token:str, edge_url:str, dimensions:int, region:str="us-west", distance_metric:str="COSINE", version:int=1):
        self.name = name
        self.key = key
        self.token = token
        self.lib_token = lib_token
        self.edge_url = edge_url
        self.region = region
        self.distance_metric = distance_metric
        self.dimensions = dimensions
        self.version = version
        self.checksum = get_checksum(self.key)

    def __str__(self):
        return self.name

    def upsert(self, input_array):
        if len(input_array) > 1000:
            raise ValueError("Cannot insert more than 1000 vectors at a time")
        checksum = get_checksum(self.key)
        encoded_array = encode(self.key, self.lib_token, self.distance_metric, self.version, input_array)
        # for vector in input_array:
        #     vector["vector"] = encode(self.key, vector["vector"])
        #     vector["meta"] = encrypt_ecb(self.key, json.dumps(vector["meta"]))

        headers = {
            'Authorization': f'{self.token}:{self.name}:{self.checksum}',
            'Content-Type': 'application/json'
        }
        data = {
            'checksum': checksum,
            'vectors': encoded_array,
        }
        print(self.edge_url)
        print(encoded_array)
        print(input_array)
        response = requests.post(f'{self.edge_url}/vector/{self.name}/upsert', headers=headers, json=data)
        print(response.text)
        if response.status_code != 200:
            raise_exception(response.status_code)
        return "Vectors inserted successfully"

    def query(self, vector, top_k=10, include_vectors=False, log=False):
        if top_k > 1000:
            raise ValueError("top_k cannot be greater than 1000")
        checksum = get_checksum(self.key)
        encoded_vector = encode_vector(key=self.key,lib_token=self.lib_token,distance_metric=self.distance_metric, version=self.version, vector=vector)
        headers = {
            'Authorization': f'{self.token}:{self.name}:{self.checksum}',
            'Content-Type': 'application/json'
        }
        data = {
            'vector': encoded_vector,
            'checksum': checksum,
            'top_k': top_k,
            'distance_metric': self.distance_metric
        }
        response = requests.post(f'{self.edge_url}/vector/{self.name}/query', headers=headers, json=data)
        if response.status_code != 200:
            raise_exception(response.status_code)
        if log == True:
            print(response.text)
        results = response.json()
        print(results)
        round_off = True
        result_array = decode(key=self.key,lib_token=self.lib_token, distance_metric=self.distance_metric, version=self.version, query_vector=vector, input_array = results)
        for result in result_array:
            if not include_vectors:
                del result["vector"]
            # if round_off:
            #     result["score"] = round(result["score"], 4)
        return result_array

    def delete_vector(self, id):
        checksum = get_checksum(self.key)
        headers = {
            'Authorization': f'{self.token}:{self.name}:{self.checksum}',
            }
        data = {
            'checksum': checksum,
        }
        response = requests.get(f'{self.edge_url}/vector/{self.name}/delete/{id}', headers=headers)
        if response.status_code != 200:
            raise_exception(response.status_code)
        return response.text + " rows deleted"
    
    # Delete multiple vectors based on a filter
    def delete_with_filter(self, filter):
        checksum = get_checksum(self.key)
        headers = {
            'Authorization': f'{self.token}:{self.name}:{self.checksum}',
            'Content-Type': 'application/json'
            }
        data = {"filter": filter}
        print(filter)
        response = requests.post(f'{self.edge_url}/vector/{self.name}/delete_with_filter', headers=headers, json=data)
        if response.status_code != 200:
            print(response.text)
            raise_exception(response.status_code)
        return response.text
