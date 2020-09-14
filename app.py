from flask import Flask ,render_template,request,url_for
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def hello_world():
    result='Please enter all the fields'
    if request.method=="POST":
        myDict=request.form
        Glucose=float(myDict['Glucose'])
        Insulin=float(myDict['Insulin'])
        Height=float(myDict['Height'])
        Weight=float(myDict['Weight'])
        Age=float(myDict['Age'])
        data=pd.read_csv("diabetes.csv")
        X=data.iloc[:,[1,4,5,7]]
        y=data.iloc[:,-1]
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=101)
    
        knn_clf=RandomizedSearchCV(estimator=KNeighborsClassifier(),param_distributions={
    "n_neighbors":[5,11],
    "metric":['euclidean','manhattan'],'weights':['uniform','distance']
    },cv=5,return_train_score=False)
        knn_clf.fit(X_train,y_train)
        data1 = {'Glucose' : Glucose, 'Insulin' : Insulin, 'BMI' : Weight/(Height**2),'Age':Age}
        test_data=pd.DataFrame(data1,index=[0])
        if (knn_clf.predict(test_data))==0:
            model_result="You do not have diabetes"
        else:
            model_result= "Model predicted Diabetes!! Make sure to visit a doctor soon"
        result ="Output:"+ model_result
    return render_template('index.html',numbers=result )

if __name__ == "__main__":
    

    app.run(debug=True)