from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtremeCls:
	"""Extreme commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extreme", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits.
			- Ripple_1: float: Max (range 1) - min (range 1)
			- Ripple_2: float: Max (range 2) - min (range 2)
			- Max_R_1_Min_R_2: float: Max (range 1) - min (range 2)
			- Max_R_2_Min_R_1: float: Max (range 2) - min (range 1)
			- Min_R_1: float: Min (range 1)
			- Max_R_1: float: Max (range 1)
			- Min_R_2: float: Min (range 2)
			- Max_R_2: float: Max (range 2)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Ripple_1'),
			ArgStruct.scalar_float('Ripple_2'),
			ArgStruct.scalar_float('Max_R_1_Min_R_2'),
			ArgStruct.scalar_float('Max_R_2_Min_R_1'),
			ArgStruct.scalar_float('Min_R_1'),
			ArgStruct.scalar_float('Max_R_1'),
			ArgStruct.scalar_float('Min_R_2'),
			ArgStruct.scalar_float('Max_R_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Ripple_1: float = None
			self.Ripple_2: float = None
			self.Max_R_1_Min_R_2: float = None
			self.Max_R_2_Min_R_1: float = None
			self.Min_R_1: float = None
			self.Max_R_1: float = None
			self.Min_R_2: float = None
			self.Max_R_2: float = None

	def read(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:ESFLatness:EXTReme \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.layer.esFlatness.extreme.read(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		Return current, average, extreme and standard deviation single-value results of the equalizer spectrum flatness
		measurement, for carrier <no>, layer/antenna <l>. See also 'Equalizer spectrum flatness limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:ESFLatness:EXTReme?', self.__class__.ResultData())

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:ESFLatness:EXTReme \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.layer.esFlatness.extreme.fetch(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		Return current, average, extreme and standard deviation single-value results of the equalizer spectrum flatness
		measurement, for carrier <no>, layer/antenna <l>. See also 'Equalizer spectrum flatness limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:ESFLatness:EXTReme?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits.
			- Ripple_1: float or bool: Limit check result for max (range 1) - min (range 1) .
			- Ripple_2: float or bool: Limit check result for max (range 2) - min (range 2) .
			- Max_R_1_Min_R_2: float or bool: Limit check result for max (range 1) - min (range 2) .
			- Max_R_2_Min_R_1: float or bool: Limit check result for max (range 2) - min (range 1) ."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float_ext('Ripple_1'),
			ArgStruct.scalar_float_ext('Ripple_2'),
			ArgStruct.scalar_float_ext('Max_R_1_Min_R_2'),
			ArgStruct.scalar_float_ext('Max_R_2_Min_R_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Ripple_1: float or bool = None
			self.Ripple_2: float or bool = None
			self.Max_R_1_Min_R_2: float or bool = None
			self.Max_R_2_Min_R_1: float or bool = None

	def calculate(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:ESFLatness:EXTReme \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.cc.layer.esFlatness.extreme.calculate(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		Return current, average and extreme limit check results for the equalizer spectrum flatness measurement, for carrier <no>,
		layer/antenna <l>. See also 'Equalizer spectrum flatness limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:ESFLatness:EXTReme?', self.__class__.CalculateStruct())
