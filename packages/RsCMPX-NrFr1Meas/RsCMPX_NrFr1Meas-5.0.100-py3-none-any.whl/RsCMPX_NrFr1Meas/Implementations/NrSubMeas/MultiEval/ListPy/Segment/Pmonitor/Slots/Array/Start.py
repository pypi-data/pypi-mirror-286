from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .........Internal.Types import DataType
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartCls:
	"""Start commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> int:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:PMONitor:SLOTs:ARRay:STARt \n
		Snippet: value: int = driver.nrSubMeas.multiEval.listPy.segment.pmonitor.slots.array.start.fetch(sEGMent = repcap.SEGMent.Default) \n
		Returns the offset of the first power monitor vs slot result for segment <no> within a result list for all measured
		segments. Such a result list is, for example, returned by the command method RsCMPX_NrFr1Meas.NrSubMeas.MultiEval.ListPy.
		Pmonitor.Slots.Rms.fetch. A returned <Start> value n indicates that the result for the first slot of the segment is the
		result (n+1) in the power result list over all segments. \n
		Suppressed linked return values: reliability \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: start: Offset of the first power monitor vs slot result."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:PMONitor:SLOTs:ARRay:STARt?', suppressed)
		return Conversions.str_to_int(response)
