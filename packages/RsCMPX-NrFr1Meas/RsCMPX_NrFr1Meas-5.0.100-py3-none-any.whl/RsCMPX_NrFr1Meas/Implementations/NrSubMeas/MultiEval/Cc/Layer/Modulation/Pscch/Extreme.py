from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtremeCls:
	"""Extreme commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extreme", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tolerance: int: No parameter help available
			- Evm_Low: float: No parameter help available
			- Evm_High: float: No parameter help available
			- Mag_Err_Low: float: No parameter help available
			- Mag_Err_High: float: No parameter help available
			- Ph_Error_Low: float: No parameter help available
			- Ph_Error_High: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Evm_Low'),
			ArgStruct.scalar_float('Evm_High'),
			ArgStruct.scalar_float('Mag_Err_Low'),
			ArgStruct.scalar_float('Mag_Err_High'),
			ArgStruct.scalar_float('Ph_Error_Low'),
			ArgStruct.scalar_float('Ph_Error_High')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Low: float = None
			self.Evm_High: float = None
			self.Mag_Err_Low: float = None
			self.Mag_Err_High: float = None
			self.Ph_Error_Low: float = None
			self.Ph_Error_High: float = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:MODulation:PSCCh:EXTReme \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.layer.modulation.pscch.extreme.fetch(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		No command help available \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:MODulation:PSCCh:EXTReme?', self.__class__.ResultData())

	def read(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:MODulation:PSCCh:EXTReme \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.layer.modulation.pscch.extreme.read(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		No command help available \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:MODulation:PSCCh:EXTReme?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tolerance: int: No parameter help available
			- Evm_Low: enums.ResultStatus2: No parameter help available
			- Evm_High: enums.ResultStatus2: No parameter help available
			- Mag_Err_Low: enums.ResultStatus2: No parameter help available
			- Mag_Err_High: enums.ResultStatus2: No parameter help available
			- Ph_Error_Low: enums.ResultStatus2: No parameter help available
			- Ph_Error_High: enums.ResultStatus2: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_enum('Evm_Low', enums.ResultStatus2),
			ArgStruct.scalar_enum('Evm_High', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mag_Err_Low', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mag_Err_High', enums.ResultStatus2),
			ArgStruct.scalar_enum('Ph_Error_Low', enums.ResultStatus2),
			ArgStruct.scalar_enum('Ph_Error_High', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Low: enums.ResultStatus2 = None
			self.Evm_High: enums.ResultStatus2 = None
			self.Mag_Err_Low: enums.ResultStatus2 = None
			self.Mag_Err_High: enums.ResultStatus2 = None
			self.Ph_Error_Low: enums.ResultStatus2 = None
			self.Ph_Error_High: enums.ResultStatus2 = None

	def calculate(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:MODulation:PSCCh:EXTReme \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.cc.layer.modulation.pscch.extreme.calculate(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		No command help available \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:MODulation:PSCCh:EXTReme?', self.__class__.CalculateStruct())
