import numpy as np
from biomimetic import ModeMOBiomimeticCell


class ModeMOBmcModel:
    def __init__(Model, name, data):
        Model.name = name
        Model.data = data
        Model.datasetRows = len(data)
        Model.output_to_inputs = {}
        for inputs, outputs in Model.data.items():
            if tuple(outputs) not in Model.output_to_inputs:
                Model.output_to_inputs[tuple(outputs)] = []
            Model.output_to_inputs[tuple(outputs)].append(inputs)
        Model.neuron_count = len(Model.output_to_inputs)
        Model.datasetModes = max(len(inputs) for inputs in Model.output_to_inputs.values())
        Model.featuresCount = len(next(iter(data.keys())))
        Model.inputNums = len(next(iter(data.keys())))
        Model.outputSize = len(next(iter(data.values())))
        Model.datasetColumns = Model.featuresCount * Model.inputNums + Model.outputSize
        Model.NeuralNetwork = []
        Model.results = []
        Model.activation_dict = {}

    def learnModel(Model):
        i = 1
        for outputs, inputs_list in Model.output_to_inputs.items():
            neuron = ModeMOBiomimeticCell(index=(1, i), inputNums=len(inputs_list[0]), 
                                          inputSize=Model.featuresCount, outputSize=Model.outputSize, 
                                          weightSize=Model.featuresCount, modeCount=len(inputs_list))
            i+=1
            neuron.learn([np.array(inputs) for inputs in inputs_list])
            neuron.output(np.array(outputs))
            Model.NeuralNetwork.append(neuron)

    def __str__(Model):
        return f"ModeMOBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Inputs: {Model.inputNums}, Features: {Model.featuresCount}, Outputs: {Model.outputSize}, Modes: {Model.datasetModes})"

    def activateModel(Model, inputValue: np.array, modeIndex):
        Model.activation_dict = {}
        Model.results = []
        activated_neurons = []
        fire_bias_array = []
        for neuron in Model.NeuralNetwork:
            if neuron.modeCount > modeIndex:
                neuron.activate(inputValue, modeIndex)
                result = neuron.fire(True)
                if all(neuron.activationFlags):
                    activated_neurons.append(neuron.index)
                    Model.results.append(result)
                    fire_bias_array.append(True)
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