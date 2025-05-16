12-Hour “Good-Enough-to-Win” Sprint
(Single-track focus: Bahamut – AI + On-chain Logic)

Goal: Ship a live end-to-end demo that meets every mandatory judging checkbox—nothing more.

0. High-level cuts
   Nice-to-have Drop it Reason
   Polkadot/XCM bridge ❌ Adds Rust + extra RPC = time killer
   Fancy UI styling ❌ Judges care about function, not Tailwind
   Multi-agent workflows ❌ One working CrewAI agent is enough
   Own backend DB ❌ Use in-memory lists / st.session_state

1. Deliverables checklist (must exist at judging table)
   File / Asset Purpose ETA
   EscrowContract.sol (see snippet ↓) Holds FTN; emits events 1 h
   Hardhat deploy script Pushes to Bahamut test-net 20 min
   oracle.js Listens to BountyPosted, runs tests, calls releaseReward() 1 h
   agent.py Single CrewAI agent (e.g., “Tax-Credit FAQ Bot”) 1.5 h
   tests/test_agent.py PyTest asserting ≥ 80 % accuracy on 3 canned Q&A 30 min
   streamlit_app.py 2 tabs ➜ “Post Bounty” & “Leaderboard” 1 h
   README.md + Loom (2 min) Submission requirement 1 h
   Canva deck (6 slides) Pitch in person 1 h
   GitHub repo (public) Open-source mandate 10 min

Total build time ≈ 8 h 30 m → leaves 3 h 30 m buffer for bugs & polish.

2. Hour-by-hour game plan
   Clock Task
   00:00 – 01:00
   Kick-off - npx hardhat init

- Paste the contract below, compile, deploy to Bahamut (RPC = https://rpc.testnet.bahamut.io/).
  01:00 – 02:20 - Write oracle.js (see skeleton).
- Test locally with Hardhat node.
  02:20 – 04:00 - Build agent.py using CrewAI quick-start; hard-code few rules.
- Write three unit tests in PyTest; make them pass.
  04:00 – 05:00 - streamlit_app.py: Tab 1 posts bounty (web3 write); Tab 2 pulls past AgentSubmitted events and prints table.
  05:00 – 06:00 - End-to-end dry run: post bounty → oracle.js auto-runs tests → calls releaseReward() → FTN arrives in dummy wallet.
  06:00 – 07:00 - Record Loom demo while everything is still fresh.
  07:00 – 08:00 - Write README.md (problem → setup → run steps).
  08:00 – 09:00 - Canva deck: ➊ Team ➋ Problem ➌ Solution ➎ Demo gif ➏ Why Bahamut ➐ Roadmap.
  09:00 – 11:30 Buffer / bug-fix / polish • add simple wallet-connect • refactor names • improve logs.
  11:30 – 12:00 Final repo push, fill Google form, breathe.

| Layer                                                        | Must-have for MVP                                                       | Why it matters                                                             | 2-line implementation hint                                        |
| ------------------------------------------------------------ | ----------------------------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **1. Bounty Escrow (Smart Contract)**                        | `postBounty()`, `submitAgent(uri)`, `releaseReward()`                   | On-chain source of truth & auto-pay; satisfies “AI + on-chain logic” track | Solidity, OpenZeppelin `PullPayment`; deploy on Bahamut test-net  |
| **2. Oracle / Verifier**                                     | Event listener → spins up CrewAI tests → calls `releaseReward()`        | Links blockchain to model evaluation; automates judging                    | 100-LOC Node/TS script (ethers.js + child-process for `pytest`)   |
| **3. CrewAI Agent Template**                                 | • `agent.py` skeleton<br>• `requirements.txt`<br>• `tests/` folder      | Gives builders a ready starting point & shows LLM in action                | Use single-agent “Tax-FAQ bot” with local Llama .cpp weights      |
| **4. Streamlit Front End**                                   | Tabs: “Create Bounty” • “Active Bounties” • “Leaderboard”               | Non-technical judges can click through the flow                            | Web3.py calls + simple `st.table`; keep styling minimal           |
| **5. Leaderboard Storage**                                   | In-contract mapping `bountyId ⇒ winningAgentCID` (and score)            | Displays who won, avoids off-chain DB for POC                              | Emit `RewardReleased` with IPFS-CID; front end listens for events |
| **6. Wallet Connect / Faucet**                               | Hard-coded sponsor acct & demo winner acct                              | Demonstrates crypto movement live                                          | Prefund with Bahamut test FTN from faucet; show balances updating |
| **7. Security Guardrails**                                   | • Allowed-models list (e.g., SHA-256 hashes)<br>• max gas & reward caps | Sells the “CRA-approved models only” story                                 | Simple `require(bytes32 == allowedHash)` in contract              |
| **8. README + Loom Demo**                                    | Clear setup & 2-min walkthrough                                         | Mandatory for submission; helps judges replay                              | Record once everything works; link in repo root                   |
| **9. Canva Slide Deck (6 slides)**                           | Team • Problem • Solution • Demo gif • Blockchain fit • Roadmap         | Evaluated during 3-min pitch                                               | Use template; drop screen recording GIF of Streamlit flow         |
| **10. Road-to-Production Hooks** _(talking point, not code)_ | KYC/KYB module • ZK-scored hidden tests • Multi-chain payout            | Shows vision beyond hackathon                                              | Mention in roadmap slide & README “Next Steps”                    |
