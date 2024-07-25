import numpy as np
from biomimetic import ParallelMOBiomimeticCell


class ParallelMOBmcModel:
  def __init__(Model, name, data: dict):
    Model.name = name
    Model.data = data
    Model.datasetRows = len(data)
    Model.inputNums = len(next(iter(data.keys())))
    Model.featuresCount = len(next(iter(next(iter(data.keys())))))
    Model.outputSize = len(next(iter(data.values())))
    Model.datasetColumns = Model.featuresCount * Model.inputNums + Model.outputSize
    Model.activation_dict = {}
    Model.results = []

  def learnModel(Model):
    Model.NeuralNetwork = []
    for index, (inputs, outputs) in enumerate(Model.data.items()):
      neuron = ParallelMOBiomimeticCell(index, len(inputs), Model.featuresCount, Model.outputSize, Model.featuresCount)
      neuron.learn(np.array(inputs))
      neuron.output(np.array(outputs))
      Model.NeuralNetwork.append(neuron)

  def __str__(Model):
    return f"PMOBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Inputs: {Model.inputNums})"

  def activateModel(Model, inputValue: np.array):
    Model.activation_dict = {}
    Model.results = []
    activated_neurons = []
    fire_bias_array = []
    for neuron in Model.NeuralNetwork:
      neuron.activate(inputValue)
      result = neuron.fire(True)
      if all(neuron.activationFlags):
        activated_neurons.append(neuron.index)
        Model.results.append(result)
        fire_bias_array.append(True)
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