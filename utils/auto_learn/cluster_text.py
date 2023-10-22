import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import random
import sys
sys.path.append('.')
from ...local_config import emb, config
openai_key = config['openai']['key']

EMBEDDING_BY = 'yiyan' # openai | bert

if EMBEDDING_BY == 'openai':
    import openai
elif EMBEDDING_BY == 'bert':
    from transformers import AutoTokenizer, AutoModelForMaskedLM
    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
    model = AutoModelForMaskedLM.from_pretrained("bert-base-chinese")
    import torch

def get_embedding(text, by=EMBEDDING_BY):
    if by == 'openai':
        # Set OpenAI API key
        openai.api_key = random.choice(openai_key) if type(openai_key) == list else openai_key
        model = "text-embedding-ada-002"
        emb_req = openai.Embedding.create(input=[text], model=model)
        embedding = emb_req.data[0].embedding
        return embedding
    elif by == 'bert':
        encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        output = model(**encoded_input)

        embedding = torch.mean(output[0], dim=1).squeeze(0)
        return embedding.detach().numpy()
    else:
        return emb(text)
    return None

def cluster_text(text_list, n_clusters=20):
    if n_clusters >= len(text_list):
        return text_list
    # Convert text_list to numerical data
    data = []
    for text in text_list:
        embedding = get_embedding(text, by=EMBEDDING_BY)
        data.append(embedding)
    data = np.array(data)

    # Cluster the data
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)

    # Get the cluster centers
    centers = kmeans.cluster_centers_

    # Get the distances to each center
    # distances = kmeans.transform(data)
    distances = euclidean_distances(data, centers)

    # Get the centers' index
    indexes = np.argmin(distances, axis=0)

    # Get the samples with the smallest distance to their center
    samples = [text_list[idx] for idx in indexes]
    return samples


def plot_clusters(text_list, n_clusters=20, openai_api_key=openai_key):
    # Set OpenAI API key
    openai.api_key = openai_api_key
    model = "text-embedding-ada-002"
    # Convert text_list to numerical data using OpenAI API
    data = []
    for text in text_list:
        emb_req = openai.Embedding.create(input=[text], model=model)
        embeddings = emb_req.data[0].embedding
        data.append(embeddings)
    data = np.array(data)

    # Cluster the data
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)

    # Reduce the dimensionality of the data
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)

    # Plot the reduced data
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=kmeans.labels_)
    for i, text in enumerate(text_list):
        plt.annotate(text, (reduced_data[i, 0], reduced_data[i, 1]))
    plt.show()


if __name__ == "__main__":
    test_data = [
        '一百多和三十的也看不出什么区别，包装精美，质量应该不错。',
        '质量很好 料子很不错 做工细致 样式好看 穿着很漂亮',
        ' 会卷的    建议买大的小的会卷   胖就别买了       没用',
        '大差了  布料很差  我也不想多说',
        '一点也不好，我买的东西拿都拿到快递员自己签收了还不给我，恶心恶心恶心，不要脸不要脸',
        '一百多和三十的也看不出什么区别，包装精美，质量应该不错。',
        '质量很好 料子很不错 做工细致 样式好看 穿着很漂亮',
        ' 会卷的    建议买大的小的会卷   胖就别买了       没用',
        '大差了  布料很差  我也不想多说',
        '一点也不好，我买的东西拿都拿到快递员自己签收了还不给我，恶心恶心恶心，不要脸不要脸',
    ]

    result = cluster_text(test_data, n_clusters=3)
    # plot_clusters(test_data, n_clusters=3)

    print(result)
