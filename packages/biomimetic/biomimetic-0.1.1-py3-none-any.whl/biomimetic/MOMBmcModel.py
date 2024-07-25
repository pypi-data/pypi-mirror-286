import numpy as np
from biomimetic import ModeOMBiomimeticCell


class ModeOMBmcModel:
    def __init__(Model, name, data: dict):
        Model.name = name
        Model.data = data
        Model.datasetRows = len(data)
        Model.datasetModes = max(len(v) for v in data.values())
        Model.featuresCount = len(next(iter(data.keys())))
        Model.outputNums = len(next(iter(data.values()))[0])
        Model.datasetColumns = Model.featuresCount + Model.outputNums * len(next(iter(data.values()))[0])
        Model.NeuralNetwork = []
        Model.results = []
        Model.activation_dict = {}

    def learnModel(Model):
        output_to_inputs = {}
        for input, output in Model.data.items():
            output = tuple(map(tuple, output))
            if output not in output_to_inputs:
                output_to_inputs[output] = []
            output_to_inputs[output].append(input)
        for output, inputs in output_to_inputs.items():
            neuron = ModeOMBiomimeticCell(index=len(Model.NeuralNetwork), inputSize=Model.featuresCount, outputSize=Model.outputNums, weightSize=Model.featuresCount, modeCount=len(inputs), outputNums=Model.outputNums)
            neuron.learn(np.array(inputs))
            neuron.output(np.array(output))
            Model.NeuralNetwork.append(neuron)


    def __str__(Model):
        return f"MOMBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Modes:{Model.datasetModes}, Outputs: {Model.outputNums})"

    def activateModel(Model, inputValue: np.array, modeIndex):
        Model.results = []
        activated_neurons = []
        fire_bias_array = []
        for neuron in Model.NeuralNetwork:
            if neuron.modeCount >= modeIndex + 1:
                neuron.activate(inputValue, modeIndex)
                result = neuron.fire(np.ones(neuron.outputNums, dtype=bool))
                if neuron.activationFlag == True:
                    activated_neurons.append(neuron.index)
                    Model.results.append(result)
                    fire_bias_array.append(np.ones(neuron.outputNums, dtype=bool))
        Model.activation_dict["Output"] = Model.results
        Model.activation_dict["Neurons"] = activated_neurons
        Model.activation_dict["Flags"] = fire_bias_array
        Model.activation_dict["Mode"] = modeIndex
        if Model.results:
            return Model.activation_dict
        Model.activation_dict["Output"] = []
        return Model.activation_dict
    
    def getActivation(Model):
        return Model.activation_dict
    
    def resetActivation(Model):
        Model.results = []
        Model.activation_dict = {}