from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaximumCls:
	"""Maximum commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability indicator'
			- Low: List[float]: EVM value for low EVM window position.
			- High: List[float]: EVM value for high EVM window position."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Low', DataType.FloatList, None, False, True, 1),
			ArgStruct('High', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Low: List[float] = None
			self.High: List[float] = None

	def read(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:EVMagnitude:PEAK:MAXimum \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.layer.evMagnitude.peak.maximum.read(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		Returns the values of the EVM peak diagrams for the OFDM symbols in the measured slot, for carrier <no>, layer/antenna
		<l>. The results of the current, average and maximum diagrams can be retrieved. There is one pair of EVM values per OFDM
		symbol, returned in the following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also
		'Square EVM'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:EVMagnitude:PEAK:MAXimum?', self.__class__.ResultData())

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default, layer=repcap.Layer.Default) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>][:LAYer<layer>]:EVMagnitude:PEAK:MAXimum \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.layer.evMagnitude.peak.maximum.fetch(carrierComponent = repcap.CarrierComponent.Default, layer = repcap.Layer.Default) \n
		Returns the values of the EVM peak diagrams for the OFDM symbols in the measured slot, for carrier <no>, layer/antenna
		<l>. The results of the current, average and maximum diagrams can be retrieved. There is one pair of EVM values per OFDM
		symbol, returned in the following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also
		'Square EVM'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param layer: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		layer_cmd_val = self._cmd_group.get_repcap_cmd_value(layer, repcap.Layer)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:LAYer{layer_cmd_val}:EVMagnitude:PEAK:MAXimum?', self.__class__.ResultData())
