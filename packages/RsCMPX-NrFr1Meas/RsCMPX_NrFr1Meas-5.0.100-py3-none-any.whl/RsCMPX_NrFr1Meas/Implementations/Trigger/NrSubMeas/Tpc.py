from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpcCls:
	"""Tpc commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpc", core, parent)

	def get_threshold(self) -> float or bool:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:THReshold \n
		Snippet: value: float or bool = driver.trigger.nrSubMeas.tpc.get_threshold() \n
		No command help available \n
			:return: trig_threshold: (float or boolean) No help available
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:TPC:THReshold?')
		return Conversions.str_to_float_or_bool(response)

	def set_threshold(self, trig_threshold: float or bool) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:THReshold \n
		Snippet: driver.trigger.nrSubMeas.tpc.set_threshold(trig_threshold = 1.0) \n
		No command help available \n
			:param trig_threshold: (float or boolean) No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(trig_threshold)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:TPC:THReshold {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.nrSubMeas.tpc.get_slope() \n
		No command help available \n
			:return: slope: No help available
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:TPC:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:SLOPe \n
		Snippet: driver.trigger.nrSubMeas.tpc.set_slope(slope = enums.SignalSlope.FEDGe) \n
		No command help available \n
			:param slope: No help available
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:TPC:SLOPe {param}')

	def get_timeout(self) -> float or bool:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:TOUT \n
		Snippet: value: float or bool = driver.trigger.nrSubMeas.tpc.get_timeout() \n
		No command help available \n
			:return: trigger_timeout: (float or boolean) No help available
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:TPC:TOUT?')
		return Conversions.str_to_float_or_bool(response)

	def set_timeout(self, trigger_timeout: float or bool) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:TOUT \n
		Snippet: driver.trigger.nrSubMeas.tpc.set_timeout(trigger_timeout = 1.0) \n
		No command help available \n
			:param trigger_timeout: (float or boolean) No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(trigger_timeout)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:TPC:TOUT {param}')

	def get_mgap(self) -> float:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:MGAP \n
		Snippet: value: float = driver.trigger.nrSubMeas.tpc.get_mgap() \n
		No command help available \n
			:return: min_trig_gap: No help available
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:TPC:MGAP?')
		return Conversions.str_to_float(response)

	def set_mgap(self, min_trig_gap: float) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:TPC:MGAP \n
		Snippet: driver.trigger.nrSubMeas.tpc.set_mgap(min_trig_gap = 1.0) \n
		No command help available \n
			:param min_trig_gap: No help available
		"""
		param = Conversions.decimal_value_to_str(min_trig_gap)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:TPC:MGAP {param}')
