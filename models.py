from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime


@dataclass
class Member:
    name: str
    contact_info: str  

@dataclass
class Transaction:
    item_name: str
    amount: float
    payer: Member
    note: str = ""
    splits: List['Split'] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now) 

    def add_split(self, split):
        self.splits.append(split)

@dataclass
class Split:
    member: Member
    share: float  # 此分帳記錄中該成員應分擔的金額

def calculate_balances(transactions: List[Transaction]) -> Dict[str, float]:
    """
    計算每個成員的總債務和應收帳款。
    返回一個字典，成員名稱為鍵，平衡值（可能為正或負）為值。
    """
    balance = {}
    for transaction in transactions:
        total_amount = transaction.amount
        num_participants = len(transaction.splits) + 1  # 包括付款人
        share_per_person = total_amount / num_participants

        # 加上付款人支付的金額
        if transaction.payer.name not in balance:
            balance[transaction.payer.name] = 0
        balance[transaction.payer.name] += total_amount - share_per_person

        # 根據分帳記錄減去每個成員應負擔的金額
        for split in transaction.splits:
            if split.member.name not in balance:
                balance[split.member.name] = 0
            balance[split.member.name] -= share_per_person

    return balance



