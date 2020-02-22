import cv2
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from utils import create_color_palette, rgb_to_hex, hex_to_rgb, rgb_list_to_hex


def get_dominant_colors(input_file, num_colors=4):
    img = cv2.imread(input_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    kmeans = KMeans(n_clusters=num_colors)
    preds = kmeans.fit_predict(img)
    colors = kmeans.cluster_centers_
    # silhouette_avg = silhouette_score(img, preds, metric='euclidean')
    # Compute the silhouette scores for each sample
    # sample_silhouette_values = silhouette_samples(X, cluster_labels)
    # print(silhouette_avg, sample_silhouette_values, colors)
    colors = colors.astype(int).tolist()   
    return rgb_list_to_hex(colors)
        
    
if __name__ == '__main__':
    img_name = './shoe1.jpg'
    colors = get_dominant_colors(img_name)
    print(colors)
    create_color_palette('./test2.jpg', colors)