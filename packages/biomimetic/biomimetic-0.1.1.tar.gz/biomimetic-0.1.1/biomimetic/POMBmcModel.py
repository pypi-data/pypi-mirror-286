import numpy as np
from biomimetic import ParallelOMBiomimeticCell



class ParallelOMBmcModel:
    def __init__(Model, name, data: dict):
        Model.name = name
        Model.data = data
        Model.datasetRows = len(data)
        Model.outputNums = len(next(iter(data.values()))[0])
        Model.featuresCount = len(next(iter(data.keys())))
        Model.datasetColumns = Model.featuresCount + Model.outputNums * len(next(iter(next(iter(data.values())))))
        Model.results = []
        Model.activation_dict = {}

    def learnModel(Model):
        Model.NeuralNetwork = []
        for index, (inputs, outputs) in enumerate(Model.data.items()):
            neuron = ParallelOMBiomimeticCell(index, Model.featuresCount, len(outputs[0]), Model.featuresCount, len(outputs))
            neuron.learn(np.array(inputs))
            neuron.output(np.array(outputs))
            Model.NeuralNetwork.append(neuron)

    def __str__(Model):
        return f"POMBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Outputs: {Model.outputNums})"

    def activateModel(Model, inputValue: np.array):
        Model.results = []
        activated_neurons = []
        fire_bias_array = []
        for neuron in Model.NeuralNetwork:
            neuron.activate(inputValue)
            result = neuron.fire(np.ones(neuron.outputNums, dtype=bool))
            if neuron.activationFlag:
                activated_neurons.append(neuron.index)
                Model.results.append(result)
                fire_bias_array.append(np.ones(neuron.outputNums, dtype=bool))
        Model.activation_dict["Output"] = Model.results
        Model.activation_dict["Neurons"] = activated_neurons
        Model.activation_dict["Flags"] = fire_bias_array
        if Model.results:
            return Model.activation_dict
        Model.activation_dict["Output"] = []
        return Model.activation_dict
    
    def getActivation(Model):
        return Model.activation_dict
    
    def resetActivation(Model):
        Model.results = []
        Model.activation_dict = {}