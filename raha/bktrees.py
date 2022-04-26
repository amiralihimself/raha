def Levenshteind(a, b):
    # Generate the length of both strings, which would be relevant in calculating the Levenshtein distance
    length1, length2 = len(a), len(b)

    # Create a table for storing the solutions as done in dynamic programming
    A = [[0 for x in range(length2 + 1)] for x in range(length1 + 1)]

    # Use dynamic programming to solve the problem in a bottom up fashion, by solving sub-problems
    for i in range(length1 + 1):
        for j in range(length2 + 1):
            if i == 0:
                A[i][j] = j
            elif j == 0:
                A[i][j] = i
            elif a[i - 1] == b[j - 1]:
                A[i][j] = A[i - 1][j - 1]
            else:
                A[i][j] = 1 + min(A[i][j - 1], A[i - 1][j], A[i - 1][j - 1])
    return A[length1][length2]



class BkTree:
    def __init__(self, dictionary, distancemetric):
#provide the modularity needed to use other distance functions (other than the edit distance)
        self.distanceMetric = distancemetric
        self.root = dictionary[0]
        self.tree = (dictionary[0], {})

    def builder(self, dictionary):
        for word in dictionary[1:]:
            self.tree = self.insertIntoTree(self.tree, word)

    def insertIntoTree(self, node, word):
        d = self.distanceMetric(word, node[0])
        if d not in node[1]:
            node[1][d] = (word, {})
        else:
            self.insertIntoTree(node[1][d], word)
        return node

    def search_for_similar_words(self, queryword, tolerance):
        #this is the main method for querying the BK-tree
        def search(node):
            distance = self.distanceMetric(queryword, node[0])
            output = []
            if distance <= tolerance:
                output.append(node[0])
            for i in range(distance - tolerance, distance + tolerance + 1):
                child = node[1]
                if i in child:
                    output.extend(search(node[1][i]))
            return output

        root = self.tree
        return search(root)


