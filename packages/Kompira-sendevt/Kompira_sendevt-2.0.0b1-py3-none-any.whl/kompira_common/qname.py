# -*- coding: utf-8 -*-
ENGINE_DISPATCH_NAME = 'engine_dispatch_queue'      # web_app -> kompirad
ENGINE_BROADCAST_NAME = 'engine_broadcast_xchg'     # web_app -> kompirad(ブロードキャスト)
ENGINE_QUEUE_FMT = 'engine_queue_{0}'

RPCQ_NAME = 'rpc_queue'              # kompirad -> jobmngrd
HBQ_NAME = 'hb_queue'                # jobmngrd -> kompirad
IOQ_NAME = 'io_queue'                # sendevt -> kompirad
CANCEL_EXCHANGE_NAME = 'cancel_xchg' # kompirad -> jobmngrd(ブロードキャスト)
JOBQ_NAME = 'job_queue'              # kompirad -> jobmngrd(ジョブマネージャ毎)


def engine_qname(engine_id):
    return ENGINE_QUEUE_FMT.format(engine_id)
