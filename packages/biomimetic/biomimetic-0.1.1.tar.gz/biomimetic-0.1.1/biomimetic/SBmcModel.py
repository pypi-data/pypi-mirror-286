import numpy as np
from biomimetic import SimpleBiomimeticCell


class SimpleBmcModel:
  def __init__(Model, name, dataTable: np.array, featuresCount):
    Model.name = name
    Model.dataset = dataTable
    Model.featuresCount = featuresCount
    Model.datasetRows = dataTable.shape[0]
    Model.datasetColumns = dataTable.shape[1]
    Model.features = dataTable[0:Model.datasetRows, 0:featuresCount]
    Model.targets = dataTable[0:Model.datasetRows, featuresCount:Model.datasetColumns]
    Model.activation_dict = {}

  def __str__(Model):
    return f"SBmcModel({Model.name}, {Model.datasetRows}, {Model.datasetColumns}, {Model.featuresCount})"

  def learnModel(Model):
    Model.NeuralNetwork = []
    for neuron in range(0, Model.datasetRows):
      Model.NeuralNetwork.append(SimpleBiomimeticCell((1, neuron),Model.features.shape[1],Model.targets.shape[1]))
      Model.NeuralNetwork[neuron].learn(Model.features[neuron])
      Model.NeuralNetwork[neuron].output(Model.targets[neuron])

  def activateModel(Model, inputValue: np.array):
    results = []
    activated_neurons = []
    for neuron in range(0, Model.datasetRows):
      Model.output = Model.NeuralNetwork[neuron].activate(inputValue)
      if Model.NeuralNetwork[neuron].activationFlag == True:
        activated_neurons.append(Model.NeuralNetwork[neuron].index)
        results.append(Model.output)
    Model.activation_dict["Output"] = results
    Model.activation_dict["Neurons"] = activated_neurons
    if results:
        return Model.activation_dict
    Model.activation_dict["Output"] = []
    return Model.activation_dict
    
  def getActivation(Model):
      return Model.activation_dict
  
  def resetActivation(Model):
      Model.activation_dict = {}