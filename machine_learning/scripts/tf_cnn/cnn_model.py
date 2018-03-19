import tensorflow as tf
import numpy as np


class CNNModel:

    def __init__(self, config):
        self.validate_config(config)
        graph, session = self.load_graph(config.ML_CNN_MODEL_FILE)
        self.graph = graph
        self.session = session
        self.input_operation = self.graph.get_operation_by_name('import/input')
        self.output_operation = self.graph.get_operation_by_name('import/final_result')
        self.labels = self.load_labels(config.ML_CNN_LABEL_FILE)
    
    def predict(self, image_path):
        """
        Takes in an image and returns a tuple with its
        categorization and a confidence level

        Args:
            image_path: the path to the image file (jpg)

        """
        img_tensor = self.read_tensor_from_image_file(image_path)
        results = self.session.run(self.output_operation.outputs[0],
                             {self.input_operation.outputs[0] : img_tensor})
        results = np.squeeze(results)
        top_result = results.argsort()[-1:][::-1][0]
        return self.labels[top_result], results[top_result]
    
    def validate_config(self, config):
        if not config.ML_CNN_MODEL_FILE and not config.ML_CNN_LABEL_FILE:
            raise AssertionError('CNN model instantiated with no configuration')

    def load_graph(self, model_file):
        with tf.Session() as persisted_sess:
            graph = tf.Graph()
            graph_def = tf.GraphDef()
            with tf.gfile.FastGFile(model_file, 'rb') as f:
                graph_def.ParseFromString(f.read())
                persisted_sess.graph.as_default()
                tf.import_graph_def(graph_def)
            return persisted_sess.graph, persisted_sess
    
    def load_labels(self, label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    # Taken from label_image.py
    def read_tensor_from_image_file(self, file_name, input_height=224, input_width=224,
                                    input_mean=128, input_std=128):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                            name='jpeg_reader')
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0);
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        result = self.session.run(normalized)
        return result

