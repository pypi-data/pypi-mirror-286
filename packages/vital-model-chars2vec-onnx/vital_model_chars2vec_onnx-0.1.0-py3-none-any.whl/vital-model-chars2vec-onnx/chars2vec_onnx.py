import os
import pickle
import numpy as np
import onnxruntime as ort


class Chars2VecONNX:
    def __init__(self, emb_dim, char_to_ix, onnx_model_path):
        if not isinstance(emb_dim, int) or emb_dim < 1:
            raise TypeError("parameter 'emb_dim' must be a positive integer")

        if not isinstance(char_to_ix, dict):
            raise TypeError("parameter 'char_to_ix' must be a dictionary")

        self.char_to_ix = char_to_ix
        self.ix_to_char = {char_to_ix[ch]: ch for ch in char_to_ix}
        self.vocab_size = len(self.char_to_ix)
        self.dim = emb_dim
        self.cache = {}

        self.session = ort.InferenceSession(onnx_model_path)

    def vectorize_words(self, words):
        if not isinstance(words, list) and not isinstance(words, np.ndarray):
            raise TypeError("parameter 'words' must be a list or numpy.ndarray")

        words = [w.lower() for w in words]
        unique_words = np.unique(words)
        new_words = [w for w in unique_words if w not in self.cache]

        if len(new_words) > 0:
            list_of_embeddings = []

            for current_word in new_words:
                if not isinstance(current_word, str):
                    raise TypeError("word must be a string")

                current_embedding = []

                for t in range(len(current_word)):
                    if current_word[t] in self.char_to_ix:
                        x = np.zeros(self.vocab_size)
                        x[self.char_to_ix[current_word[t]]] = 1
                        current_embedding.append(x)
                    else:
                        current_embedding.append(np.zeros(self.vocab_size))

                list_of_embeddings.append(np.array(current_embedding))

            max_len = max(map(len, list_of_embeddings))
            embeddings_pad_seq = np.array([np.pad(embed, ((0, max_len - len(embed)), (0, 0)), 'constant') for embed in list_of_embeddings], dtype=np.float32)

            input_name = self.session.get_inputs()[0].name

            for i, current_word in enumerate(new_words):
                input_data = np.expand_dims(embeddings_pad_seq[i], axis=0)
                result = self.session.run(None, {input_name: input_data})
                self.cache[current_word] = result[0][0]

        word_vectors = [self.cache[current_word] for current_word in words]

        return np.array(word_vectors)

    @classmethod
    def load_model(cls):

        path_to_model = os.path.dirname(os.path.abspath(__file__)) + '/models/' + 'en_300'
        path_to_onnx = os.path.dirname(os.path.abspath(__file__)) + '/models/' + 'en_300/' + 'model.onnx'

        with open(path_to_model + '/model.pkl', 'rb') as f:

            structure = pickle.load(f)

            if len(structure) == 2:  # Ensure it contains emb_dim and char_to_ix
                emb_dim, char_to_ix = structure
                cache = {}  # Initialize an empty cache if not saved
            elif len(structure) == 3:
                emb_dim, char_to_ix, cache = structure
            else:
                raise ValueError("Unexpected structure in model.pkl")

            # emb_dim, char_to_ix, cache = structure[0], structure[1], structure[2]

        c2v_model = Chars2VecONNX(emb_dim, char_to_ix, path_to_onnx)

        c2v_model.cache = cache

        return c2v_model
