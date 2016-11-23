# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generate melodies from a trained checkpoint of a melody RNN model."""

import ast
import os
import time

# internal imports

import tensorflow as tf
import magenta

from magenta.models.melody_rnn import melody_rnn_config_flags
from magenta.models.melody_rnn import melody_rnn_model
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

class MelodyGenerator(object):

  def get_checkpoint(self):
    return 'checkpoint_file'

  def get_bundle(self):
    bundle_file = '/magenta-models/lookback_rnn.mag'
    return magenta.music.read_bundle_file(bundle_file)

  def steps_to_seconds(self, steps, qpm):
    steps_per_quarter = 4
    return steps * 60.0 / qpm / steps_per_quarter


  def generate(self, generator):
    beam_size           = 1
    branch_factor       = 1
    midi_path           = '/usr/src/audio/current.mid'
    num_steps           = 128
    steps_per_iteration = 1
    temperature         = 1.0

    qpm = magenta.music.DEFAULT_QUARTERS_PER_MINUTE
    primer_melody = magenta.music.Melody([60])
    primer_sequence = primer_melody.to_sequence(qpm=qpm)

    total_seconds = steps_to_seconds(num_steps, qpm)

    generator_options = generator_pb2.GeneratorOptions()

    input_sequence = primer_sequence
    last_end_time = (max(n.end_time for n in primer_sequence.notes) if primer_sequence.notes else 0)
    generate_section = generator_options.generate_sections.add( start_time=last_end_time + steps_to_seconds(1, qpm), end_time=total_seconds)

    if generate_section.start_time >= generate_section.end_time:
      tf.logging.fatal( 'Priming sequence is longer than the total number of steps')
      return

    generator_options.args['temperature'].float_value = temperature
    generator_options.args['beam_size'].int_value = beam_size
    generator_options.args['branch_factor'].int_value = branch_factor
    generator_options.args['steps_per_iteration'].int_value = steps_per_iteration

    tf.logging.debug('input_sequence: %s', input_sequence)
    tf.logging.debug('generator_options: %s', generator_options)

    generated_sequence = generator.generate(input_sequence, generator_options)
    magenta.music.sequence_proto_to_midi_file(generated_sequence, midi_path)

  def getMelody(self):
    """Saves bundle or runs generator based on flags."""
    tf.logging.set_verbosity(FLAGS.log)

    config = melody_rnn_config_flags.config_from_flags()
    generator = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
        model=melody_rnn_model.MelodyRnnModel(config),
        details=config.details,
        steps_per_quarter=FLAGS.steps_per_quarter,
        checkpoint=get_checkpoint(),
        bundle=get_bundle())

    if FLAGS.save_generator_bundle:
      bundle_filename = os.path.expanduser(FLAGS.bundle_file)
      if FLAGS.bundle_description is None:
        tf.logging.warning('No bundle description provided.')
      tf.logging.info('Saving generator bundle to %s', bundle_filename)
      generator.create_bundle_file(bundle_filename, FLAGS.bundle_description)
    else:
      generate(generator)
