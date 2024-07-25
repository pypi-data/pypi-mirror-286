import numpy as np
from biomimetic import ModeMMBiomimeticCell


class ModeMMBmcModel:
  def __init__(Model, name, data: dict):
    Model.name = name
    Model.data = data
    Model.datasetRows = len(data)
    Model.output_to_inputs = {}
    Model.results = []
    for inputs, outputs in Model.data.items():
            outputs = tuple(tuple(row) for row in outputs)
            if tuple(outputs) not in Model.output_to_inputs:
                Model.output_to_inputs[tuple(outputs)] = []
            Model.output_to_inputs[tuple(outputs)].append(inputs)
    Model.neuron_count = len(Model.output_to_inputs)
    Model.datasetModes = max(len(inputs) for inputs in Model.output_to_inputs.values())
    Model.inputNums = len(next(iter(data.keys())))
    Model.outputNums = len(next(iter(data.values())))
    Model.featuresCount = len(next(iter(next(iter(data.keys())))))
    Model.outputSize = len(next(iter(next(iter(data.values())))))
    Model.datasetColumns = Model.featuresCount * Model.inputNums + Model.outputSize * Model.outputNums
    Model.activation_dict = {}

  def learnModel(Model, MMMBmcModelDataSetAllocations):
    Model.NeuralNetwork = []
    i = 1
    for outputs, inputs_list in Model.output_to_inputs.items():
      neuron = ModeMMBiomimeticCell(index=(1, i), inputNums=len(inputs_list[0]), inputSize=Model.featuresCount, outputSize=len(outputs[0]), outputNums=Model.outputNums, weightSize=Model.featuresCount, modeCount=len(inputs_list))
      i+=1
      neuron.learn([np.array(inputs) for inputs in inputs_list])
      neuron.allocate(MMMBmcModelDataSetAllocations)
      neuron.output(np.array(outputs))
      Model.NeuralNetwork.append(neuron)

  def __str__(Model):
    return f"MMMBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Inputs: {Model.inputNums}, Outputs: {Model.outputNums}, Modes: {Model.datasetModes})"

  def activateModel(Model, inputValue: np.array, modeIndex):
    Model.results = []
    activated_neurons = []
    fire_bias_2D_array = []
    for neuron in Model.NeuralNetwork:
      if neuron.modeCount >= modeIndex + 1:
        neuron.activate(inputValue, modeIndex)
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