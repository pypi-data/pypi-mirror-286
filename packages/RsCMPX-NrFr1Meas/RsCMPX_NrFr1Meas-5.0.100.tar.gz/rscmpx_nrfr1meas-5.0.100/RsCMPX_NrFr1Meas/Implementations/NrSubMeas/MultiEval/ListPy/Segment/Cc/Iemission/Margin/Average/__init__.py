from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	@property
	def rbIndex(self):
		"""rbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIndex'):
			from .RbIndex import RbIndexCls
			self._rbIndex = RbIndexCls(self._core, self._cmd_group)
		return self._rbIndex

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check
			- Margin: float: Margin over all non-allocated RBs (scope of general limit component)
			- Iq_Image: float: Margin at image frequencies of allocated RBs (scope of I/Q image limit component)
			- Carr_Leakage: float: Margin at the carrier frequency (scope of I/Q offset limit component)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Margin'),
			ArgStruct.scalar_float('Iq_Image'),
			ArgStruct.scalar_float('Carr_Leakage')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin: float = None
			self.Iq_Image: float = None
			self.Carr_Leakage: float = None

	def fetch(self, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:CC<Carrier>]:IEMission:MARGin:AVERage \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.segment.cc.iemission.margin.average.fetch(sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Return the in-band emission limit line margin results for segment <no> in list mode, for carrier <c>. The CURRent margins
		indicate the minimum (vertical) distance between the limit line and the current trace. A negative result indicates that
		the limit is exceeded. The AVERage, EXTReme and SDEViation values are calculated from the current margins. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:IEMission:MARGin:AVERage?', self.__class__.FetchStruct())

	def clone(self) -> 'AverageCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AverageCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
