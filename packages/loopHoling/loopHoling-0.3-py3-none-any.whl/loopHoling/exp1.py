def code():

    codee = """import pandas as pd
                import numpy as np
                data = pd.read_csv('C:/Users/Students/Desktop/trainingexamples.csv')
                ass = data
                features = np.array(data)[:,:-1]
                print("features in the database:\n",features)
                target = np.array(data)[:,-1]
                print("target concept:\n",target)
                for i,val in enumerate(target):
                    if val == 'Yes':
                        hypothesis = features[i].copy()
                        break
                print(hypothesis)
                for i,val in enumerate(features):
                    if target[i] == 'Yes':
                        for x in range (len(hypothesis)):
                            if val[x] != hypothesis[x]:
                                hypothesis[x] = '?'
                                
                print(hypothesis)"""
    return codee

