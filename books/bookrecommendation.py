from .models import Book,Comment,Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
def update_clusters():
    num_comments = Comment.objects.count()
    print (num_comments)
    update_step = 1
    print (update_step)
    if num_comments % update_step == 0: 
        # Create a sparse matrix from user comments
        all_user_names = User.objects.values_list('id', flat=True)
        all_book_ids = Comment.objects.values_list('book_id', flat=True)
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_book_ids)+1), dtype=np.float32)
        for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_comments = Comment.objects.filter(user_id=all_user_names[i])
            for user_comment in user_comments:
                ratings_m[i,user_comment.book_id] = user_comment.rating

        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())

        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before referring to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(id=all_user_names[i]))

        print (new_clusters)
