import numpy as np
from biomimetic import ParallelMMBiomimeticCell


class ParallelMMBmcModel:
  def __init__(Model, name, data: dict):
    Model.name = name
    Model.data = data
    Model.datasetRows = len(data)
    Model.inputNums = len(next(iter(data.keys())))
    Model.outputNums = len(next(iter(data.values())))
    Model.featuresCount = len(next(iter(next(iter(data.keys())))))
    Model.outputSize = len(next(iter(next(iter(data.values())))))
    Model.datasetColumns = Model.featuresCount * Model.inputNums + Model.outputSize * Model.outputNums
    Model.activation_dict = {}
    Model.results = []

  def learnModel(Model, PMMBmcModelDataSetAllocations):
    Model.NeuralNetwork = []
    for index, (inputs, outputs) in enumerate(Model.data.items()):
      neuron = ParallelMMBiomimeticCell(index=(1, index), inputNums=len(inputs), inputSize=Model.featuresCount, outputSize=len(outputs[0]), outputNums=Model.outputNums, weightSize=Model.featuresCount)
      neuron.learn(np.array(inputs))
      neuron.allocate(PMMBmcModelDataSetAllocations)
      neuron.output(np.array(outputs))
      Model.NeuralNetwork.append(neuron)

  def __str__(Model):
    return f"PMMBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Inputs: {Model.inputNums}, Outputs: {Model.outputNums})"

  def activateModel(Model, inputValue: np.array):
    Model.results = []
    activated_neurons = []
    fire_bias_2D_array = []
    for neuron in Model.NeuralNetwork:
      neuron.activate(inputValue)
      fireBiases = np.ones(shape=Model.outputNums, dtype=bool)
      for output_index, input_indices in neuron.allocationDict.items():
        if all(neuron.activationFlags[input_indices]):
          continue
        else:
          fireBiases[output_index] = False
      activated_neurons.append(neuron.index)
      fire_bias_2D_array.append(fireBiases)
      result = neuron.fire(fireBiases)
      Model.results.append(result)
    Model.activation_dict["Output"] = Model.results
    Model.activation_dict["Neurons"] = activated_neurons
    Model.activation_dict["Flags"] = fire_bias_2D_array
    if Model.results:
      return Model.activation_dict
    Model.activation_dict["Output"] = []
    return Model.activation_dict
  
    
  def getActivation(Model):
     return Model.activation_dict
  
  def resetActivation(Model):
     Model.results = []
     Model.activation_dict = {}