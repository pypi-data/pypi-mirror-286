from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtoleranceCls:
	"""Ptolerance commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: PowerStep, default value after init: PowerStep.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptolerance", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_powerStep_get', 'repcap_powerStep_set', repcap.PowerStep.Nr1)

	def repcap_powerStep_set(self, powerStep: repcap.PowerStep) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PowerStep.Default
		Default value after init: PowerStep.Nr1"""
		self._cmd_group.set_repcap_enum_value(powerStep)

	def repcap_powerStep_get(self) -> repcap.PowerStep:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, power_tolerance: List[float], powerStep=repcap.PowerStep.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:SRS:LIMit:PTOLerance<PowerStep> \n
		Snippet: driver.configure.nrSubMeas.srs.limit.ptolerance.set(power_tolerance = [1.1, 2.2, 3.3], powerStep = repcap.PowerStep.Default) \n
		No command help available \n
			:param power_tolerance: No help available
			:param powerStep: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ptolerance')
		"""
		param = Conversions.list_to_csv_str(power_tolerance)
		powerStep_cmd_val = self._cmd_group.get_repcap_cmd_value(powerStep, repcap.PowerStep)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:SRS:LIMit:PTOLerance{powerStep_cmd_val} {param}')

	def get(self, powerStep=repcap.PowerStep.Default) -> List[float]:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:SRS:LIMit:PTOLerance<PowerStep> \n
		Snippet: value: List[float] = driver.configure.nrSubMeas.srs.limit.ptolerance.get(powerStep = repcap.PowerStep.Default) \n
		No command help available \n
			:param powerStep: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ptolerance')
			:return: power_tolerance: No help available"""
		powerStep_cmd_val = self._cmd_group.get_repcap_cmd_value(powerStep, repcap.PowerStep)
		response = self._core.io.query_bin_or_ascii_float_list(f'CONFigure:NRSub:MEASurement<Instance>:SRS:LIMit:PTOLerance{powerStep_cmd_val}?')
		return response

	def clone(self) -> 'PtoleranceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PtoleranceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
