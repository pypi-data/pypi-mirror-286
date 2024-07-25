# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================
import os,sys
import json
import requests
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt
import time


# LLAMA-2 interface
"""
The LAMMA class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
Llama 2
From Meta

Welcome to the official Hugging Face organization for Llama 2 models from Meta! In order to access models here, please visit the Meta website and accept our license terms and acceptable use policy before requesting access to a model. Requests will be processed within 1-2 days.

Llama 2 is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases. Llama-2-Chat models outperform open-source chat models on most benchmarks we tested, and in our human evaluations for helpfulness and safety, are on par with some popular closed-source models like ChatGPT and PaLM.

Read our paper, learn more about the model, or get started with code on GitHub.

https://ai.meta.com/llama/
"""

class LLAMA3(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):
        
        self.start_time = time.time()
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "LLAMA3",
            "model" : "meta-llama/Llama-2-7b-chat-hf",
            "credentials" : "key.json"
        }
       
        
    
    # Get Text
    def get_content(self, collected_messages):

        """
        Get the text from the collected stream of chunks
        """  
        # Combine all messages from chunks
        
        try:
            full_text = ''.join(collected_messages)
        except Exception as e:
            print("LLAMA3: error get_content() {0}" .format(str(e)))
            return('your prompt returned no response  as {}'.format(e))
        
        try:
            if self.is_code(full_text):
                #print("LLAMA3: {0} response: {1}" .format(self.__class__.__name__,str(full_text)))
                return str(full_text), True
            else:
                return str(full_text), False
        except Exception as e:
            #print("LLAMA3 ERROR is_code() {0} Response Type {1}" .format(str(e), type(full_text)))
            return('LLAMA3 {0} response failed as {1}'.format(self.model,str(e)))
        

    

    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        
        """Predict using a Large Language Model."""
        project_id = "llama3"
        location = "us-central1"
        
        if self.url is not None:
            url = self.url
        else:
            url = "http://localhost/llama3/predict"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """

        try:
            """ Call API """
            
            ## See if we can invoke importToDb
            headers = {"Content-Type" :  "application/json"}
            prmpt = prompt.get_string() + " , please return response in markdown format"
            
            
            # Chec if thread of conversation exists.. 
            messages=[]
            if convid:
                qa = super().get_conversation_history(convid,"LLAMA3")
                for q,a in qa:
                    messages.append( {"role": "user", "content" : q})
                    messages.append( {"role": "assistant", "content" : a})
        
            messages.append( {"role": prompt.get_role(), "content" : prmpt } )
            if prompt.context:
                messages.append({"role": prompt.get_role(), "content" : prompt.get_context()})
        

            values = {'question':  messages}

            try:
                response = requests.post(url, data=json.dumps(values),headers=headers,stream=True)
            except Exception as e:
                #print("Couldn't fetch response from llama3")
                print(f"Exception caught is: {e}")
                response = None
            collected_messages = []
            #print("llama3: response type {0}" .format(type(response)))
            #print("llama3 r.content {0}" .format(type(response.text)))
            elapsed_time = time.time() - self.start_time
            print("llama3: first token: {0}" .format(elapsed_time))
            for chunk in response:
                chunk_message = chunk.decode('utf-8')
                extra = '<eos>'
                chunk_message = chunk_message.replace(extra, '')
                #print(chunk_message)
                #print("type of chunk {0}" .format(type(chunk)))
                
                #if chunk.choices[0].delta and chunk.choices[0].delta.content:
                   #chunk_message = chunk.choices[0].delta.content

                collected_messages.append(chunk_message)
                self.stream_to_redis(chunk_message, taskid)
                #print(chunk_message or "", end="", flush=True)

            collected_messages = [m for m in collected_messages if m is not None]


            if not response:
                return None, None
            else:
                try:
                    content, is_code = self.get_content(collected_messages)
                except Exception as e:
                    print("LLAMA3: error: get_content()..{0}" .format(str(e)))
                content = content.replace(prmpt, "")
                extras = ['<|start_header_id|>','<|start_header_id|>','<|eot_id|>']
                for extra in extras:          
                    content = content.replace(extra, '')
                if content and taskid:
                    self.publish_to_redis(content, taskid)
                #print("collected_messages {0}" .format(collected_messages))
                return (content), is_code
            

            
        except Exception as e:
            print('error calling {0}: {1}' .format(self.model, str(e)))
            return None, None

