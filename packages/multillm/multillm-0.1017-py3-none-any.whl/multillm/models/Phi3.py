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



# microsoft/Phi-3-mini-128k-instruct"
"""
The Phi-3-Mini-128K-Instruct is a 3.8B parameters, lightweight, state-of-the-art open model trained with the Phi-3 datasets that includes both synthetic data
and the filtered publicly available websites data with a focus on high-quality and reasoning dense properties. 
The model belongs to the Phi-3 family with the Mini version in two variants 4K and 128K which is the context length 
(in tokens) that it can support.

The model has underwent a post-training process that incorporates both supervised fine-tuning and direct preference optimization for the
 instruction following and safety measures. When assessed against benchmarks testing common sense, language understanding, 
math, code, long context and logical reasoning, Phi-3 Mini-4K-Instruct showcased a robust and state-of-the-art 
performance among models with less than 13 billion parameters.

Resources and Technical Documentation:

Phi-3 Microsoft Blog
Phi-3 Technical Report
Phi-3 on Azure AI Studio
Phi-3 ONNX: 128K
"""

class PHI3(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

        self.start_time = time.time()
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "PHI3",
            "model" : "microsoft/Phi-3-mini-128k-instruct",
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
            print("GEMMA: error get_content() {0}" .format(str(e)))
            return('your prompt returned no response  as {}'.format(e))

        try:
            if self.is_code(full_text):
                #print("PH13: {0} response: {1}" .format(self.__class__.__name__,str(full_text)))
                return str(full_text), True
            else:
                return str(full_text), False
        except Exception as e:
            #print("PH13 ERROR is_code() {0} Response Type {1}" .format(str(e), type(full_text)))
            return('PHI3 {0} response failed as {1}'.format(self.model,str(e)))
        

    
    
    
    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        
        """Predict using a Large Language Model."""
        project_id = "phi3"
        location = "us-central1"
        
        if self.url is not None:
            url = self.url
        else:
            url = "http://localhost/phi3/predict"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """

        try:
            """ Call API """
            
            ## See if we can invoke importToDb
            headers = {"Content-Type" :  "application/json"}
            prmpt = prompt.get_string() + " , please return response in markdown format"
            
            
            # Chec if thread of conversation exists.. 
            messages=[]
            if convid:
                qa = super().get_conversation_history(convid,"PHI3")
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
                #print("Couldn't fetch response from Gemma")
                print(f"Exception caught is: {e}")
                response = None
            collected_messages = []
            #print("Ph13: response type {0}" .format(type(response)))
            #print("Ph13 r.content {0}" .format(type(response.text)))
            elapsed_time = time.time() - self.start_time
            print("Phi3: first token: {0}" .format(elapsed_time))
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
                    print("PH13: error: get_content()..{0}" .format(str(e)))
                content = content.replace(prmpt, "")
                extras = ['<eos>','<bos>','<start_of_turn>user','<start_of_turn>','<start_of_turn>model',
                          '<end_of_turn>model','<end_of_turn>','<s>', '</s>', '[INST]', '[/INST]' ]
                for extra in extras:          
                    content = content.replace(extra, '')
                if content and taskid:
                    self.publish_to_redis(content, taskid)
                #print("collected_messages {0}" .format(collected_messages))
                return (content), is_code
            

            
        except Exception as e:
            print('error calling {0}: {1}' .format(self.model, str(e)))
            return None, None
        
        
