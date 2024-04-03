import sklearn
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def get_content_recommendations(id, wt, top_n=10):
    final_df = pd.read_csv("final_df.csv")
    idx = final_df[final_df['product id'] == id].index[0]
    
    similarity = cosine_similarity(final_df.iloc[:, 2:])
    similarity_scores = { final_df['product id'][i]:similarity[idx][i]*wt for i in range(83) }
    similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    return similarity_scores[1:6]

def get_furr():
   df1 = pd.read_csv("Furniture preferences (Responses) - Form responses 1.csv")
   df1 = df1.drop(['Timestamp', 'Email address'], axis=1)
   furr = []
   for i in range(25):
       furr.append((df1.iloc[i, 5]+", "+df1.iloc[i, 6]+", "+df1.iloc[i, 7]+", "+df1.iloc[i, 8]+", "+df1.iloc[i, 9]).split(", "))
   return furr
   

def get_collaborative_recommendations(id, wt, top_n=5):
    cf_df = pd.read_csv("cf_df.csv")
    similarity1 = cosine_similarity(cf_df)
    similarity_scores1 = list(similarity1[id])
    temp = pd.DataFrame()
    temp['user_id'] = [i for i in range(25)]
    temp['score'] = cosine_similarity(cf_df)[id]
    temp['wishlisted'] = get_furr()
    temp = temp.sort_values(by=['score'], ascending=False)
    dic = {}
    for i in range(2, 6):
      for j in temp['wishlisted'][i]:
        if(j not in dic):
          dic[j] = []
        dic[j].append(temp['score'][i])
    final = []
    for key, value in dic.items():
      simi = np.mean(np.array(value))*wt
      final.append((key, simi))
    sorted_final = sorted(final, key = lambda x: x[1], reverse=True)

    return(sorted_final)

def hybrid(furniture, user_id):
  df = pd.read_csv("furniture1.csv")
  df = df[["breadth", "category", "color", "height", "image link", "length", "material", "price", "product", "product id", "product image ", "product link", "support color"]]
  array = []
  for i in furniture:
    array += get_content_recommendations(i, 0.3)
    array += get_collaborative_recommendations(user_id, 0.6)
    sorted_array = sorted(array, key = lambda x: x[1], reverse=True)
  new_df = pd.DataFrame()
  furr_name = []
  for j in sorted_array:
    furr_name.append(j[0])
  new_df['product id'] = furr_name
  return pd.merge(new_df, df, how ='left', on ='product id').to_dict(orient='records')

