from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MschemeCls:
	"""Mscheme commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mscheme", core, parent)

	def set(self, mod_scheme: enums.ModulationScheme, carrierComponent=repcap.CarrierComponent.Nr1, allocation=repcap.Allocation.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:ALLocation<Allocation>:PUSCh:MSCHeme \n
		Snippet: driver.configure.nrSubMeas.cc.allocation.pusch.mscheme.set(mod_scheme = enums.ModulationScheme.AUTO, carrierComponent = repcap.CarrierComponent.Nr1, allocation = repcap.Allocation.Default) \n
		No command help available \n
			:param mod_scheme: No help available
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
		"""
		param = Conversions.enum_scalar_to_str(mod_scheme, enums.ModulationScheme)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:MSCHeme {param}')

	# noinspection PyTypeChecker
	def get(self, carrierComponent=repcap.CarrierComponent.Nr1, allocation=repcap.Allocation.Default) -> enums.ModulationScheme:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:ALLocation<Allocation>:PUSCh:MSCHeme \n
		Snippet: value: enums.ModulationScheme = driver.configure.nrSubMeas.cc.allocation.pusch.mscheme.get(carrierComponent = repcap.CarrierComponent.Nr1, allocation = repcap.Allocation.Default) \n
		No command help available \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
			:return: mod_scheme: No help available"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:MSCHeme?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationScheme)
