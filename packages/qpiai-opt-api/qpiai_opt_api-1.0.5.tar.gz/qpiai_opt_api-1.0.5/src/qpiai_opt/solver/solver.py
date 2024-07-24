from urllib import response
from pydantic import BaseModel
import pickle
import requests
from requests.models import Response
import json


class Solver:
    """
    Solver class connects to QpiAI-Opt's cloud server, and run the solver on the passed problem.

    Initialize Solver class with problem and access token

    :type problem: BaseModel
    :param problem: Problem object to be passed from one of the classes in problem directory

    :type url: str
    :param url: Url to access api

    :type access_token: str
    :param access_token: access token to authenticate the solver
    """
    response: Response

    def __init__(self, problem: BaseModel, url: str, access_token: str):
        self.Problem = problem
        self.data = pickle.dumps(problem)
        self.url = url
        self.access_token = access_token
        self.response = None
        self.graph = None


    def run(self, queue=False):
        """
        Runs the problem on the QpiAI-Opt Solver on cloud and receives the response
        """
        if queue:
            response = requests.post(url=f"{self.url}/job/{self.Problem.problem_type}",
                                      headers={"access_token": self.access_token}, data=self.data)
            response = response.json()
            print(response)

            if response["job_id"]:
                self.job_id = response["job_id"]

        else:
          self.job_id = None
          self.response = requests.post(url=f"{self.url}/{self.Problem.problem_type}",
                                        headers={"access_token": self.access_token}, data=self.data)

    def get_qubo_graph(self):
        if self.response:
            try:
                self.graph = self.response.json()['graph']
                return self.response.json()['graph']
            except:
                return self.response
        else:
            print("No response received! Make sure to run the Solver.run() method before accessing response metadata!")

    def get_result(self):
        """
        to fetch the result after the solver has returned the result of the submitted problem

        :return Response: json
        """
        if self.job_id:
            response = requests.get(url=f"{self.url}/job/{self.job_id}",
                                      headers={"access_token": self.access_token})
            response = response.json()
            self.response = json.loads(response["response"])
            if response["status"] == 'SUCCESS':
                result = {'num_nodes': self.response['num_nodes'],
                          'objective': self.response['objective'],
                          'time': self.response['time']}
                return result
            else:
                status = response["status"]
                self.status = status
                print(f"Job Id : {self.job_id} returned with status {status}, {self.response}")
        else:
          if self.response.status_code == 202:
            result = {'num_nodes': self.response.json()['num_nodes'],
                      'objective': self.response.json()['objective'],
                      'time': self.response.json()['time']}
            return result
          else:
            print(f"[ERROR] {self.response.json()['detail']}")
            return


    def get_solution(self):
        if self.response is None:
            print(f"job is {self.status}")
            return None

        if isinstance(self.response, dict):
            # Print the entire response if it's a dictionary
            # Check for an error detail
            if 'detail' in self.response:
                print(self.response['detail'])
                return 
            # Return the solution if it exists
            return self.response.get('solution')
        
        elif isinstance(self.response, str):
            try:
                # Parse the string as JSON
                parsed_response = json.loads(self.response)
                # Print the parsed response
                # Check for an error detail
                if 'detail' in parsed_response:
                    print(parsed_response['detail'])
                    return None
                # Return the solution if it exists
                return parsed_response.get('solution')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None  # Or handle the error in a way that's appropriate for your application

        elif isinstance(self.response, Response):
          if self.response.status_code == 202:
            return self.response.json()['solution']
          else:
            print(f"[ERROR] {self.response.json()['detail']}")
            return
        else:
            print(f"Unsupported response type: {type(self.response)}")
            return None

    
    def get_qubo_dict(self):
        self.qubo_dict = dict()
        if self.response:
            try:
                self.graph = self.response.json()['graph']
                if self.graph:
                    l = len(self.graph["weights"])
                    for i in range(l):
                        self.qubo_dict[(self.graph["edges"][0][i], self.graph["edges"][1][i])] = self.graph["weights"][i]
                    return self.qubo_dict
            except:
                # print(e)
                return self.response
        else:
            print("No response received! Make sure to run the Solver.run() method before accessing response metadata!")

