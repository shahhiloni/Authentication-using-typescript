from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "blockchain-course-content.pdf"

sections = [
    ("Blockchain Course Content", ["Beginner to Intermediate | Hinglish | 8 Weeks | Self-paced or Instructor-led"]),
    ("Course Objective", ["Is course ka goal learners ko blockchain ki basic theory, practical use cases, wallet concepts, smart contracts, DApps, security practices, aur career roadmap samjhana hai.", "Course complete karne ke baad learner blockchain ecosystem ko clearly explain kar sakega aur basic decentralized application ka plan bana sakega."]),
    ("Target Audience", ["Students jo blockchain technology start karna chahte hain.", "Developers jo Web3 aur smart contracts seekhna chahte hain.", "Business professionals jo blockchain use cases samajhna chahte hain.", "Beginners jinko cryptocurrency aur decentralized systems ka overview chahiye."]),
    ("Prerequisites", ["Basic computer knowledge.", "Internet aur browser usage ka experience.", "Programming knowledge helpful hai, lekin mandatory nahi.", "Developer track ke liye JavaScript / TypeScript basics recommended hain."]),
]
weeks = [
("Week 1: Blockchain Fundamentals", ["Blockchain kya hai?", "Centralized, decentralized, aur distributed systems.", "Blocks, transactions, hashes, nonce, aur chain structure.", "Immutability aur transparency.", "Public vs private blockchains."], "Ek simple block diagram banaiye: transaction data, previous hash, current hash, timestamp, aur nonce."),
("Week 2: Cryptography Basics", ["Hashing kya hoti hai?", "SHA-256 ka high-level overview.", "Public key aur private key ka role.", "Digital signatures.", "Wallet address kaise banta hai?"], "Online hash generator me text ka hash banakar observe kariye ki small change se output completely change hota hai."),
("Week 3: Consensus Mechanisms", ["Consensus ki need kyun hoti hai?", "Proof of Work.", "Proof of Stake.", "Validators, miners, staking, gas fees.", "Forks aur finality."], "Proof of Work aur Proof of Stake ke pros and cons ki comparison table banaiye."),
("Week 4: Cryptocurrency and Wallets", ["Cryptocurrency kya hai?", "Coins vs tokens.", "Hot wallet vs cold wallet.", "Seed phrase aur backup practices.", "Exchanges, custody, aur self-custody."], "Ek testnet wallet setup ka written walkthrough banaiye. Real funds use na karein."),
("Week 5: Smart Contracts", ["Smart contract kya hota hai?", "Ethereum Virtual Machine ka overview.", "Solidity introduction.", "Contract deployment lifecycle.", "Events, functions, state variables, aur gas."], "Simple voting system ka paper design banaiye: voters, candidates, vote count, aur restrictions."),
("Week 6: Decentralized Applications", ["DApp kya hota hai?", "Frontend, wallet, smart contract, aur blockchain node interaction.", "Web3 libraries ka overview.", "Oracles ka role.", "DApp UX challenges."], "Ek DApp idea choose karke architecture draw kariye: frontend, wallet, contract, data source."),
("Week 7: Blockchain Use Cases", ["Finance and payments.", "Supply chain tracking.", "Identity management.", "NFTs and digital ownership.", "Healthcare records.", "Governance and voting."], "Ek use case select karke likhiye: blockchain kyun useful hai, stakeholders kaun hain, aur risks kya hain?"),
("Week 8: Security, Legal Awareness, and Career Roadmap", ["Common scams: phishing, fake airdrops, rug pulls.", "Smart contract vulnerabilities.", "Audit ka importance.", "Regulatory awareness.", "Career paths: developer, auditor, product manager, analyst, community manager.", "Learning roadmap and portfolio ideas."], "Apna 30-day blockchain learning plan banaiye jisme reading, practice, project, aur portfolio tasks hon."),
]
for title, topics, activity in weeks:
    sections.append((title, ["Topics:"] + [f"- {t}" for t in topics] + ["Learning Outcomes:", "- Learner key concepts simple language me explain kar sakega.", "- Learner practical examples aur limitations identify kar sakega.", f"Activity: {activity}"]))
sections += [
    ("Capstone Project Ideas", ["1. Simple token concept document.", "2. Decentralized voting system design.", "3. Supply chain tracking workflow.", "4. NFT certificate issuing platform plan.", "5. Crypto wallet security checklist website."]),
    ("Assessment Plan", ["Weekly quiz: 20%", "Practical activities: 30%", "Final capstone project: 40%", "Participation / discussion: 10%"]),
    ("Recommended Tools", ["Browser-based blockchain explorers.", "Testnet wallet.", "Remix IDE for Solidity practice.", "GitHub for portfolio.", "Documentation from major blockchain platforms."]),
    ("Safety Note", ["Learning ke liye testnets ka use karein. Real private keys, seed phrases, ya real funds kisi demo ya practice activity me share na karein."]),
]

class PDF:
    def __init__(self):
        self.objects=[]; self.pages=[]; self.font_obj=None
    def add_obj(self, data):
        self.objects.append(data); return len(self.objects)
    def text_escape(self, s):
        return s.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
    def add_page(self, lines):
        cmds=["BT", "/F1 10 Tf", "50 792 Td", "14 TL"]
        for text, size, bold in lines:
            cmds.append(f"/F1 {size} Tf")
            cmds.append(f"({self.text_escape(text)}) Tj")
            cmds.append("T*")
        cmds.append("ET")
        stream="\n".join(cmds).encode('latin-1','replace')
        content=self.add_obj(b"<< /Length "+str(len(stream)).encode()+b" >>\nstream\n"+stream+b"\nendstream")
        page=self.add_obj(f"<< /Type /Page /Parent 0 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 {self.font_obj} 0 R >> >> /Contents {content} 0 R >>".encode())
        self.pages.append(page)
    def build(self):
        self.font_obj=self.add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        page_lines=[]
        def emit(text, size=10, bold=False):
            nonlocal page_lines
            for part in textwrap.wrap(text, width=88) or [""]:
                page_lines.append((part, size, bold))
                if len(page_lines)>=52:
                    self.add_page(page_lines); page_lines=[]
        for title, paras in sections:
            emit("", 10); emit(title, 15, True)
            for p in paras: emit(p, 10)
        if page_lines: self.add_page(page_lines)
        kids=" ".join(f"{p} 0 R" for p in self.pages).encode()
        pages_obj=self.add_obj(b"<< /Type /Pages /Kids ["+kids+b"] /Count "+str(len(self.pages)).encode()+b" >>")
        for p in self.pages:
            self.objects[p-1]=self.objects[p-1].replace(b"/Parent 0 0 R", f"/Parent {pages_obj} 0 R".encode())
        catalog=self.add_obj(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>".encode())
        out=bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offsets=[]
        for i,obj in enumerate(self.objects,1):
            offsets.append(len(out)); out+=f"{i} 0 obj\n".encode()+obj+b"\nendobj\n"
        xref=len(out); out+=f"xref\n0 {len(self.objects)+1}\n0000000000 65535 f \n".encode()
        for off in offsets: out+=f"{off:010d} 00000 n \n".encode()
        out+=f"trailer\n<< /Size {len(self.objects)+1} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
        return bytes(out)

OUT.write_bytes(PDF().build())
print(f"Generated {OUT}")
