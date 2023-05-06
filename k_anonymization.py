import pandas as pd
import numpy as np

def main(data, categories_module, k, output_folder_path, clusters_callback=None, generalize_data=True):

    taxonomy_trees = categories_module.taxonomy_trees
    data = categories_module.data
    numeric_attrs = categories_module.numeric_attributes
    categorical_attrs = categories_module.categories

    def get_lowest_common_ancestor_subtree(values, tree):
        if 'tree' in tree:
            tree = tree['tree']

        if tree['value'] in values:
            return tree

        if 'children' in tree:
            matching_subtrees = [get_lowest_common_ancestor_subtree(values, child) for child in tree['children']]
            matching_subtrees = list(filter(None, matching_subtrees))

            if len(matching_subtrees) == 1:
                return matching_subtrees[0]
            elif len(matching_subtrees) > 1:
                return tree
        return None




    def height(tree):
        if not tree:
            return 0
        children = tree.get('children', [])
        return 1 + max([height(child) for child in children], default=0)







    def IL(cluster, numeric_attrs, categorical_attrs, taxonomy_trees):
        info_loss = 0
        # print("IL cluster:", cluster)

        for attr in numeric_attrs:
            domain_size = cluster[attr].max() - cluster[attr].min()
            if domain_size > 0:
                info_loss += (cluster[attr].max() - cluster[attr].min()) / abs(domain_size)

        for i, attr in enumerate(categorical_attrs):
            union_set = set(cluster[attr])
            tree = taxonomy_trees[i]
            subtree = get_lowest_common_ancestor_subtree(union_set, tree)
            info_loss += height(subtree) / height(tree)

        return info_loss * len(cluster)





    def find_best_record(S, C, numeric_attrs, categorical_attrs, taxonomy_trees, class_penalty):
        min_diff = float('inf')
        best_record = None

        for index, row in S.iterrows():
            c = pd.concat([C, pd.DataFrame([row], columns=S.columns)])  # Updated this line

            c_class_label = c["label"].mode()[0]
            r_class_label = row["label"]

            if c_class_label == r_class_label:
                diff = IL(c, numeric_attrs, categorical_attrs, taxonomy_trees) - IL(C, numeric_attrs, categorical_attrs, taxonomy_trees)
            else:
                diff = IL(c, numeric_attrs, categorical_attrs, taxonomy_trees) - IL(C, numeric_attrs, categorical_attrs, taxonomy_trees) + class_penalty

            if diff < min_diff:
                min_diff = diff
                best_record = row

        return best_record





    def greedy_k_member_clustering(data, k, numeric_attrs, categorical_attrs, taxonomy_trees, progress_callback=None,
                                   clusters_callback=None):

        S = data.copy()
        clusters = []

        while not S.empty:
            # Initialize a new cluster with the first k records
            records = S.sample(n=k)
            cluster = records
            S = S.drop(records.index)

            while len(cluster) < 2 * k - 1 and not S.empty:
                record = find_best_record(S, cluster, numeric_attrs, categorical_attrs, taxonomy_trees,
                                          class_penalty=1.0)  # Adjust the class_penalty value as needed

                if record is not None:
                    cluster = pd.concat([cluster, record.to_frame().T])
                    S = S.drop(record.name)
                else:
                    break

            clusters.append(cluster)

            if progress_callback is not None:
                progress_callback(len(clusters))

            if clusters_callback is not None:
                clusters_callback(len(clusters))

            # Check if there are less than k records left
            if len(S) < k:
                # Distribute remaining records among existing clusters
                while not S.empty:
                    record = S.iloc[0]
                    S = S.drop(record.name)
                    cluster_idx = 0
                    min_diff = float('inf')
                    best_cluster = 0  # Initialize best_cluster to 0

                    for i, c in enumerate(clusters):
                        if len(c) < 2 * k - 1:
                            diff = IL(pd.concat([c, record.to_frame().T]), numeric_attrs, categorical_attrs,
                                      taxonomy_trees) - IL(c, numeric_attrs, categorical_attrs, taxonomy_trees)
                            if diff < min_diff:
                                min_diff = diff
                                best_cluster = i

                    clusters[best_cluster] = pd.concat([clusters[best_cluster], record.to_frame().T])
                    if clusters_callback is not None:
                        clusters_callback(len(clusters))

        return clusters, len(clusters)




    ####GENERALISATION####

    def generalize_clusters(clusters, numeric_attrs, categorical_attrs, taxonomy_trees):
        generalized_data = []
        for cluster in clusters:
            # Get the set of unique values for each categorical attribute in the cluster
            categorical_values = {}
            for attr in categorical_attrs:
                categorical_values[attr] = set(cluster[attr].unique())

            # Generalize numeric attributes
            generalized_numeric_attrs = {}
            for attr in numeric_attrs:
                min_value = cluster[attr].min()
                max_value = cluster[attr].max()
                generalized_numeric_attrs[attr] = f"{min_value} - {max_value}"

            # Generalize categorical attributes
            generalized_categorical_attrs = {}
            for attr in categorical_attrs:
                tree = next((tree for tree in taxonomy_trees if tree['attribute'] == attr), None)
                if tree is not None:
                    # Get the lowest common ancestor subtree for the values of the current attribute
                    values = categorical_values[attr]
                    generalized_subtree = get_lowest_common_ancestor_subtree(values, tree)
                    if generalized_subtree is not None:
                        generalized_value = generalized_subtree['value']
                        generalized_categorical_attrs[attr] = generalized_value
                    else:
                        print(f"Warning: Unable to find a common ancestor for the attribute '{attr}' with values {values}. Skipping generalization for this attribute in the current cluster.")

            # Add a "count" column to each row of the cluster with the value equal to the number of records in the cluster
            cluster['count'] = len(cluster)

            # Create a new row for the cluster with the generalized attributes and the count of records in that cluster
            row = {**generalized_numeric_attrs, **generalized_categorical_attrs, 'count': len(cluster)}
            generalized_data.append(row)

        return pd.DataFrame(generalized_data)



    #
    #test on smaller sample
    sample_data = data.sample(n=200, random_state=42)

    # Call the greedy_k_member_clustering function
    trees = [tree['tree'] for tree in taxonomy_trees]
    clusters, total_clusters = greedy_k_member_clustering(sample_data, k, numeric_attrs, categorical_attrs, trees,
                                                          clusters_callback=clusters_callback)

    # Sort clusters based on information loss
    sorted_clusters = sorted(clusters, key=lambda c: IL(c, numeric_attrs, categorical_attrs, trees))

    # Calculate and print the information loss for each cluster
    total_information_loss = 0
    for i, cluster in enumerate(sorted_clusters):
        il = IL(cluster, numeric_attrs, categorical_attrs, trees)
        total_information_loss += il

    # ...

    if generalize_data:
        generalized_data = generalize_clusters(sorted_clusters, numeric_attrs, categorical_attrs, taxonomy_trees)
    else:
        # Combine all clusters into a single DataFrame without generalization
        generalized_data = pd.concat(sorted_clusters)

    # Save the generalized data to a CSV file
    output_file_name = "generalized_data.csv" if generalize_data else "ungeneralized_data.csv"
    output_path = f"{output_folder_path}/{output_file_name}"
    generalized_data.to_csv(output_path, index=False)
    print(f"Saved Data to {output_path}")

    # Add a return statement to return the generalized data
    return generalized_data, total_clusters