import time
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('figure',max_open_warning = 0)
from pylab import rcParams
from PIL import Image
from scipy.cluster.hierarchy import dendrogram, linkage

# Load pose-dataset
data = pd.read_csv('60activitiesposedata.csv', header=0)
coordinates = data.columns[1:]

print(data)
print(coordinates)

# Extract joint
joint_list = []
for i in np.arange(1,36,3):
    joint_code = data.columns[i][3:]
    joint_list.append(joint_code)
activity_list = data['name']
print('joint name:', joint_list)
print('activity name:', activity_list)

# Create a dataframe of lists of xyz coordinate data for 12 joints at t=0 to N-1
act_df = data.iloc[:,1:]
d = {}
for e in range(len(activity_list)):
    temp_df = [np.array(act_df.iloc[e,:][i].strip('[]').split(','), dtype = np.float64) for i in range(len(coordinates))]
    d[e] = temp_df
act_df = pd.DataFrame(d)
print(act_df)

act_df_X = act_df[::3].reset_index(drop=True).T
act_df_Y = act_df[1::3].reset_index(drop=True).T
act_df_Z = act_df[2::3].reset_index(drop=True).T

# Create joint angle
# Create joint node
joint_node = [[0, 1],[0, 2],[0, 6],[1, 3],[1, 7],[2, 4],[3, 5],[6, 7],[6, 8],[7, 9],[8, 10],[9, 11]]


# Get degree of moving joints

angle_list = [(1, 0, 2), (0, 1, 3), (0, 2, 4), (1, 3, 5), (0, 6, 8), (1, 7, 9), (6, 8, 10), (7, 9, 11)]
angle_name_list = [[joint_node[i_a[0]],joint_node[i_a[1]],joint_node[i_a[2]]] for i_a in angle_list]

df_features = pd.DataFrame()
for act in range(60):
    for i in range(8):
        #degree_=dict_angles[act][i]
        df_features = pd.concat([df_features,
                                 pd.DataFrame(np.array([act,
                                                        #i,
                                                        #np.mean(degree_).round(2),
                                                        #np.std(degree_).round(2),
                                                        #(np.max(degree_)-np.min(degree_)),
                                                        #(np.std(degree_)/np.mean(degree_)).round(2)])).T],
                                                        i],
                                                        axis=0)
df_freatures.columns =

# Create a dict of degree  for
dict_angles = {}
for act in range(len(activity_list)):

# Create a list of angles per activity
    angle = []
    for idx in angle_list:
        a = np.array([act_df_X.iloc[act, :][idx[0]], act_df_Y.iloc[act, :][idx[0]], act_df_Z.iloc[act, :][idx[0]]])
        b = np.array([act_df_X.iloc[act, :][idx[1]], act_df_Y.iloc[act, :][idx[1]], act_df_Z.iloc[act, :][idx[1]]])
        c = np.array([act_df_X.iloc[act, :][idx[2]], act_df_Y.iloc[act, :][idx[2]], act_df_Z.iloc[act, :][idx[2]]])

# Create vector
    vec_a = a - b
    vec_c = c - b

# Cosine = dot product of two vectors divded by product of magnitude of two vectors
# compute of magnitude of two vectors, a and c
#    vec_a = vec_a.flatten()
#    length_vec_a = []
#    for i in range(len(vec_a[0])):
#        length_vec_a.append(np.linalg.norm([vec_a_[i],vec_a_[i+len(vec_a[0])],vec_a_[i+len(vec_a[0])*2]]))
#    lenth_vec_a = np.array(length_vec_a)
#
#    vec_c = vec_c.flatten()
#    length_vec_c = []
#    for i in range(len(vec_c[0])):
#        length_vec_c.append(np.linalg.norm([vec_c_[i],vec_a_[i+len(vec_c[0])],vec_c_[i+len(vec_c[0])*2]]))
#    lenth_vec_c = np.array(length_vec_c)

#    inner_product = []
#    for i in range(len(vec_c[0])):
#        inner_product.append(np.inner([vec_a_[i], vec_a_[i + len(vec_a[0])], vec_a_[i + len(vec_a[0]) * 2]],
#                                      [vec_c_[i], vec_c_[i + len(vec_c[0])], vec_c_[i + len(vec_c[0]) * 2]]))
#    inner_product = np.array(inner_product)

#    cos = inner_product/(length_vec_a * lenth_vec_c)

#    rad = np.arccos(cos)
#    degree = np.rad2deg(rad).astype(int)
#    angles.append(degree)

#dict_angles[act] = np.array(angle)



def get_animation(activity) -> str:
    act_idx = activity_list[activity_list == activity].index.values
    X = act_df_X.iloc[act_idx,:].values
    Y = act_df_Y.iloc[act_idx,:].values
    Z = act_df_Z.iloc[act_idx,:].values

    #get ses of index of moving joints from features dataframe that matchs with activity_idx and label ==1
    moving_joint_idx = df_features[(df_fratures['activity_idx']==act_idx[0]) & (df_features['label']==1)]['joint_idx'].astype(int).values
    moving_angles = [angle_list[idx] for idx in moving_joint_idx]
    moving_joints = [[list(e[:2]),list(e[1:])] for e in moving_angles]
    moving_joints = [e for item in moving_joints for e in item]

    image = []
    for t in range(len(X[0][0])-1):
        X_t = [col[i][t] for col in X for i in range(12)]
        Y_t = [col[i][t] for col in Y for i in range(12)]
        Z_t = [col[i][t] for col in Z for i in range(12)]

        ax = plt.axes(projection='3d')
        rcParams['figure.figsize'] = 5,5

        fig = plt.figure()
        for idx in idx_joint:
            ax.plot([X_t[idx[0]], X_t[idx[1]]], [Y_t[idx[0]], Y_t[idx[1]]], [Z_t[idx[0]], Z_t[idx[1]]], c='red')
        for idx in moving_joints:
            ax.plot([X_t[idx[0]], X_t[idx[1]]], [Y_t[idx[0]], Y_t[idx[1]]], [Z_t[idx[0]], Z_t[idx[1]]], c='yellow')
        ax.scatter3D(X_t, Y_t, Z_t, c='green')

        ax.axes.set_xlim3d(left=0, right=1)
        ax.axes.set_ylim3d(bottom=0, top=1)
        ax.axes.set_zlim3d(bottom=-1, top=1)
        ax.tick_params(labelbotttom=False, labelleft=False)
        ax.margins(0)
        plt.loff()
        images.append(fig)
        plt.clf()

    images.argb = [fig2data(fig) for fig in images]
    images_pil = [Image.fromarray(img) for img in images_argb]
    images_pil[0].save("{}.gif",format(str(actvity)),save_all=True, append_images=images_pil,duration=40,loop=0)

def activity_select():
    idx=int(input('enter activity index:'))
    print(activity_list[idx])
    return activity_list[idx]

get_animation('arnold press')













