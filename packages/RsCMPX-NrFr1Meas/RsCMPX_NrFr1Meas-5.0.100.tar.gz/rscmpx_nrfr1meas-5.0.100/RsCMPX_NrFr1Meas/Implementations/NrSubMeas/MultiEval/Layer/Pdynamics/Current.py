from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability indicator'
			- Out_Of_Tolerance: int: Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count for power dynamics measurements exceeding the specified power limits.
			- Off_Power_Before: float: No parameter help available
			- On_Power_Rms: float: No parameter help available
			- On_Power_Peak: float: No parameter help available
			- Off_Power_After: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Off_Power_Before'),
			ArgStruct.scalar_float('On_Power_Rms'),
			ArgStruct.scalar_float('On_Power_Peak'),
			ArgStruct.scalar_float('Off_Power_After')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Off_Power_Before: float = None
			self.On_Power_Rms: float = None
			self.On_Power_Peak: float = None
			self.Off_Power_After: float = None

	def read(self, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation[:LAYer<layer>]:PDYNamics:CURRent \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.layer.pdynamics.current.read(layer = repcap.Layer.Default) \n
		Return the single-value results of the power dynamics measurement. The current, average, minimum, maximum and standard
		deviation results can be retrieved. The OFF power results refer to antenna <l>. The ON power results refer to the sum of
		both antenna signals. \n
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:LAYer{layer_cmd_val}:PDYNamics:CURRent?', self.__class__.ResultData())

	def fetch(self, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:LAYer<layer>]:PDYNamics:CURRent \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.layer.pdynamics.current.fetch(layer = repcap.Layer.Default) \n
		Return the single-value results of the power dynamics measurement. The current, average, minimum, maximum and standard
		deviation results can be retrieved. The OFF power results refer to antenna <l>. The ON power results refer to the sum of
		both antenna signals. \n
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LAYer{layer_cmd_val}:PDYNamics:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tolerance: int: No parameter help available
			- Off_Power_Before: float or bool: No parameter help available
			- On_Power_Rms: float or bool: No parameter help available
			- On_Power_Peak: float or bool: No parameter help available
			- Off_Power_After: float or bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float_ext('Off_Power_Before'),
			ArgStruct.scalar_float_ext('On_Power_Rms'),
			ArgStruct.scalar_float_ext('On_Power_Peak'),
			ArgStruct.scalar_float_ext('Off_Power_After')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Off_Power_Before: float or bool = None
			self.On_Power_Rms: float or bool = None
			self.On_Power_Peak: float or bool = None
			self.Off_Power_After: float or bool = None

	def calculate(self, layer=repcap.Layer.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation[:LAYer<layer>]:PDYNamics:CURRent \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.layer.pdynamics.current.calculate(layer = repcap.Layer.Default) \n
		No command help available \n
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LAYer{layer_cmd_val}:PDYNamics:CURRent?', self.__class__.CalculateStruct())
