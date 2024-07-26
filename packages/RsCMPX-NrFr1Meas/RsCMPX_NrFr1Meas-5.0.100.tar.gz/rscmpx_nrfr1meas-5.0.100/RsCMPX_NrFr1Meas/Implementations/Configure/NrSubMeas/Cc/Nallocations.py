from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NallocationsCls:
	"""Nallocations commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nallocations", core, parent)

	def set(self, number: int, carrierComponent=repcap.CarrierComponent.Nr1) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:NALLocations \n
		Snippet: driver.configure.nrSubMeas.cc.nallocations.set(number = 1, carrierComponent = repcap.CarrierComponent.Nr1) \n
		Number of allocations to be configured, for carrier <no>. \n
			:param number: For the measured carrier, only 1 is allowed.
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
		"""
		param = Conversions.decimal_value_to_str(number)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:NALLocations {param}')

	def get(self, carrierComponent=repcap.CarrierComponent.Nr1) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:NALLocations \n
		Snippet: value: int = driver.configure.nrSubMeas.cc.nallocations.get(carrierComponent = repcap.CarrierComponent.Nr1) \n
		Number of allocations to be configured, for carrier <no>. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:return: number: For the measured carrier, only 1 is allowed."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:NALLocations?')
		return Conversions.str_to_int(response)
