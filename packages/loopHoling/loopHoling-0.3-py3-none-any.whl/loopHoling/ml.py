def code1():

    codee = """
            import pandas as pd
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


def code2():

    codee = """
            import numpy as np
            import pandas as pd
            data = pd.DataFrame(data=pd.read_csv('data.csv'))

            concepts = np.array(data.iloc[:,0:-1])
            target= np.array(data.iloc[:,-1])
            def learn(concepts, target):
                specific_h = concepts[0].copy()
                general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
                for i,h in enumerate(concepts):
                    if target[i] == 'yes':
                        for x in range(len(specific_h)):
                            if h[x]!= specific_h[x]:
                                specific_h[x] = '?'
                                general_h[x][x] = '?'
                    if target[i] == 'no':
                        for x in range(len(specific_h)):
                            if h[x] != specific_h[x] :
                                general_h[x][x] = specific_h[x]
                            else:
                                general_h[x][x] = '?'
                indices = [i for i, val in enumerate(general_h) if val == ['?','?','?','?','?','?']]
                for i in indices:
                    general_h.remove(['?','?','?','?','?','?'])
                return specific_h, general_h
            s_final, g_final = learn(concepts, target)
            print('Final S: ', s_final, sep="\n")
            print('Final G: ', g_final, sep="\n")"""
    return codee

def code3():

    codee = """
            import numpy as np 
            import pandas as pd
            dataset = pd.read_csv('C:/Users/Students/Desktop/data.csv')
            print(dataset)
            def entropy(target):
                elements,counts = np.unique(target,return_counts = True)
                entropy = np.sum([(-counts[i]/np.sum(counts))*np.log2(counts[i]/np.sum(counts))for i in range(len(elements))])
                return entropy
            def InfoGain(data,split_attribute_name,target_name = "Decision"):
                total_entropy = entropy(data[target_name])
                vals,counts= np.unique(data[split_attribute_name],return_counts=True)
                Weighted_Entropy = np.sum([(counts[i]/np.sum(counts))*entropy(data.where(data[split_attribute_name]==vals[i]).dropna()[target_name])for i in range(len(vals))])
                InfoGain = total_entropy-Weighted_Entropy
                return InfoGain
            def ID3(data,originaldata,features,target_attribute_name="Decision",parent_node_class = None):
                if len(np.unique(data[target_attribute_name]))<=1:
                    return np.unique(data[target_attribute_name])[0]
                elif len(data) == 0:
                    return np.unique(originaldata[target_attribute_name])[np.argmax(np.unique(originaldata[target_attribute_name],return_counts = True)[1])]
                elif len(features)==0:
                    return parent_node_class
                else:
                    parent_node_class=np.unique(data[target_attribute_name])[np.argmax(np.unique(data[target_attribute_name],return_counts = True)[1])]
                    items_values=[InfoGain(data,feature,target_attribute_name) for feature in  features]
                    best_feature_index = np.argmax(items_values)
                    best_feature = features[best_feature_index]
                tree = {best_feature:{}}
                features =[i for i in features if i != best_feature]
                for value in np.unique(data[best_feature]):
                    value = value
                    sub_data = data.where(data[best_feature]== value).dropna()
                    subtree = ID3(sub_data,dataset,features,target_attribute_name,parent_node_class)
                    tree[best_feature][value]= subtree
                return(tree)
            tree = ID3(dataset,dataset,dataset.columns[:-1])
            print('\n Display Tress:\n',tree)"""
    return codee

def code4():

    codee = """
            import numpy as np 

            x = np.array(([2,9],[1,5],[3,6]),dtype=float)
            y = np.array(([92],[86],[89]),dtype=float)

            x = x/np.amax(x,axis=0)
            y = y/100

            def sigmoid(x):
                return 1/(1+np.exp(-x))
                        
            def derivatives_sigmoid(x):
                return x*(1-x)

            epoch = 900
            lr = 1.5

            inputlayer_neuron = 2
            hiddenlayer_neuron = 3
            output_neuron = 1
            wh = np.random.uniform(size =(inputlayer_neuron,hiddenlayer_neuron))
            bh = np.random.uniform(size =(1,hiddenlayer_neuron))
            wout = np.random.uniform(size =(hiddenlayer_neuron,output_neuron))
            bout = np.random.uniform(size =(1,output_neuron))

            for i in range(epoch):
                hinp1 = np.dot(x,wh)
                hinp = hinp1 + bh
                hlayer_act  = sigmoid(hinp)
                outinp1 = np.dot(hlayer_act,wout)
                outinp = outinp1 + bout
                output = sigmoid(outinp)
                EO = y-output
                outgrad = derivatives_sigmoid(output)
                
                d_output = EO*outgrad
                EH = d_output.dot(wout.T)
                hiddengrad = derivatives_sigmoid(hlayer_act)
                

            d_hiddenlayer =EH * hiddengrad

            wout += hlayer_act.T.dot(d_output)*lr
            bout += np.sum(d_output,axis=0,keepdims=True)*lr
            wh += x.T.dot(d_hiddenlayer)*lr
            bh += np.sum(d_hiddenlayer,axis = 0, keepdims = True)*lr
            print("input: \n " + str(x))
            print("Actual Output : \n" + str(y))
            print("Predicted output: \n",output)"""
    return codee

def code5():

    codee = """
            import pandas as pd
            from sklearn import tree
            from sklearn.preprocessing import LabelEncoder
            from sklearn.naive_bayes import GaussianNB

            data = pd.read_csv('tennisdata.csv')
            print("The first 5 Values of data is :\n", data.head())

            X = data.iloc[:, :-1]
            print("\nThe First 5 values of the train data is\n", X.head())
            y = data.iloc[:, -1]
            print("\nThe First 5 values of train output is\n", y.head())

            le_outlook = LabelEncoder()
            X.Outlook = le_outlook.fit_transform(X.Outlook)
            le_Temp = LabelEncoder()
            X.Temp= le_Temp.fit_transform(X.Temp)
            le_Humidity = LabelEncoder()
            X.Humidity = le_Humidity.fit_transform(X.Humidity)
            le_Wind = LabelEncoder()
            X.Wind = le_Wind.fit_transform(X.Wind)
            print("\nNow the Train output is\n", X.head())
            le_PlayTennis = LabelEncoder()
            y = le_PlayTennis.fit_transform(y)

            print("\nNow the Train output is\n",y)
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.50)
            classifier = GaussianNB()
            classifier.fit(X_train, y_train)

            from sklearn.metrics import accuracy_score
            print("Accuracy is:", accuracy_score(classifier.predict(X_train), y_train))
            print("Accuracy is:", accuracy_score(classifier.predict(X_test), y_test))"""
    return codee


def code6():

    codee = """
            import numpy as np
            import csv
            import pandas as pd

            from pgmpy.models import BayesianModel
            from pgmpy.estimators import MaximumLikelihoodEstimator
            from pgmpy.inference import VariableElimination

            heartD=pd.read_csv('heart.csv')
            heartD=heartD.replace('?',np.nan)

            print('few examples from the dataset are given below')
            print(heartD.head())

            model=BayesianModel([('age','trestbps'),('age','fbs'),
                                ('gender','trestbps'),('exang','trestbps'),('trestbps','heartdisease'),('fbs','heartdisease'),
                                ('heartdisease','restecg'),('heartdisease','thalach'),('heartdisease','chol')])
            print("\nlearning cpd using maximum likelihood estimator")
            model.fit(heartD,estimator=MaximumLikelihoodEstimator)

            print("\ninfering with bayesian network:")
            HeartDisease=VariableElimination(model)

            print("\n 1.probabilityof heartdisease given age=30")
            q=HeartDisease.query(variables=['heartdisease'],evidence={'age':35})
            print(q)

            print("\n2.probability of heartdisease given cholestrol=100")
            c=HeartDisease.query(variables=['heartdisease'],evidence={'chol':241})
            print(c)
                        """


    return codee

def code7():

    codee = """
            from sklearn.cluster import KMeans
            from sklearn import preprocessing
            from sklearn.mixture import GaussianMixture
            from sklearn.datasets import load_iris
            import sklearn.metrics as sm
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt

            dataset = load_iris()

            X = pd.DataFrame(dataset.data)
            X.columns=['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
            y = pd.DataFrame(dataset.target)
            y.columns = ['Targets']

            plt.figure(figsize=(14,7))
            colormap=np.array(['red','lime','black'])
            plt.subplot(1,3,1)
            plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y.Targets],s=40)
            plt.title('Real')

            plt.subplot(1,3,2)
            model=KMeans(n_clusters=3)
            model.fit(X)
            predY = np.choose(model.labels_,[0,1,2]).astype(np.int64)
            plt.scatter(X.Petal_Length,X.Petal_Width,c = colormap[predY],s=40)
            plt.title('KMeans')

            scaler = preprocessing.StandardScaler()
            scaler.fit(X)
            xsa = scaler.transform(X)
            xs = pd.DataFrame(xsa,columns=X.columns)
            gmm = GaussianMixture(n_components=3)
            gmm.fit(xs)
            y_cluster_gmm=gmm.predict(xs)
            plt.subplot(1,3,3)
            plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y_cluster_gmm],s=40)
            plt.title('GMM Classification')
            """
    
    return codee

def code8():

    codee = """
            import numpy as np
            import matplotlib.pyplot as plt
            import pandas as pd
            from sklearn.datasets import load_iris

            dataset = load_iris()
            X = dataset.data
            y = dataset.target

            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            from sklearn.neighbors import KNeighborsClassifier
            classifier = KNeighborsClassifier(n_neighbors=5)
            classifier.fit(X_train, y_train)

            accuracy = classifier.score(X_test, y_test)
            accuracy1 = classifier.score(X_train, y_train)

            print(accuracy)
            print(accuracy1)

            example = np.array([5.7,3,4.2,1.2])
            example = example.reshape(1,-1)
            print(example)

            pred = classifier.predict(example)
            print(pred)

            x_new = np.array([[5,2.9,1,0.2]])

            from sklearn.metrics import confusion_matrix
            from sklearn.metrics import accuracy_score
            from sklearn.metrics import classification_report

            y_pred = classifier.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            print(cm)

            print("Correct Prediction", accuracy_score(y_test, y_pred))
            print("Wrong Prediction", (1-accuracy_score(y_test, y_pred)))

                        """
    return codee

def code9():

    codee = """
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np

            def kernel(point,xmat,k):
                m,n = np.shape(xmat)
                weights = np.mat(np.eye((m)))
                for j in range(m):
                    diff = point - X[j]
                    weights[j,j] = np.exp(diff*diff.T/(-2.0*k**2))

                return weights
            def localWeight(point, xmat, ymat, k):
                weights = kernel(point, xmat, k)
                W = (xmat.T * (weights * xmat)).I * (xmat.T * (weights * ymat.T))
                return W
                
            def localWeightRegression(xmat,ymat,k):
                m,n = np.shape(xmat)
                ypred = np.zeros(m)
                for i in range(m):
                    ypred[i] = xmat[i]*localWeight(xmat[i],xmat,ymat,k)
                return ypred

            data = pd.read_csv(r'10-dataset.csv')
            bill = np.array(data.total_bill)
            tip = np.array(data.tip)

            mbill = np.mat(bill)
            mtip = np.mat(tip)

            m = np.shape(mbill)[1]
            one = np.mat(np.ones(m))
            X = np.hstack((one.T,mbill.T))

            ypred = localWeightRegression(X,mtip,0.5)
            SortIndex = X[:,1].argsort(0)
            xsort = X[SortIndex][:,0]

            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.scatter(bill,tip,color = 'green')
            ax.plot(xsort[:,1],ypred[SortIndex],color = 'red',linewidth = 5)
            plt.xlabel = ('Total bill')
            plt.ylabel('Tip')
            plt.show();
                        """
    return codee

def code10():

    codee = """
            import numpy as np
            import matplotlib.pyplot as plt
            import pandas as pd

            df = pd.read_csv('Downloads/Social_Network_Ads.csv')

            X = df.iloc[:, [2,3]]
            y = df.iloc[:, 4]

            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

            print("Training data : ", X_train.shape)
            print("Testing data : ", X_test.shape)

            from sklearn.preprocessing import StandardScaler
            sc_X = StandardScaler()
            X_train = sc_X.fit_transform(X_train)
            X_test = sc_X.fit_transform(X_test)

            from sklearn.svm import SVC
            classifier = SVC(kernel='linear', random_state=0)
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)

            from sklearn import metrics
            print("Accuracy Score : with linear kernel")
            print(metrics.accuracy_score(y_test, y_pred))


            classifier = SVC(kernel='rbf')
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)
            print("Accuracy Score : with default rbf kernel")
            print(metrics.accuracy_score(y_test, y_pred))

            classifier = SVC(kernel='rbf', gamma=15, C=7, random_state=0)
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)
            print("Accuracy Score On test data : with default rbf kernel")
            print(metrics.accuracy_score(y_test, y_pred))

            svc = SVC(kernel='poly', degree=4)
            svc.fit(X_train, y_train)
            y_pred = svc.predict(X_test)
            print("Accuracy Score : with poly kernel and degree")
            print(metrics.accuracy_score(y_test, y_pred))

            import matplotlib.pyplot as plt
            plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train)
            plt.xlabel('Age')
            plt.ylabel('Estimated Salary')
            plt.title('Training Data')
            plt.show()

            plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
            plt.xlabel('Age')
            plt.ylabel('Estimated Salary')
            plt.title('Test Data')
            plt.show()

            classifier = SVC(kernel='linear', random_state=0)
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)

            plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
            plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train)

            w = classifier.coef_[0]
            a = -w[0]/w[1]
            xx = np.linspace(-2.5, 2.5)
            yy = a * xx -(classifier.intercept_[0])/w[1]

            plt.plot(xx,yy)
            plt.axis("off")
            plt.show();
                        """
    return codee