## What a Financial Market Actually Is

A financial market is any venue—physical or electronic—where buyers and sellers trade financial claims: ownership stakes (equities), promises to repay debt (bonds), contracts whose value derives from something else (derivatives), currencies (FX), and raw-material exposure (commodities). Markets exist to do two jobs: move capital from those who have it (savers) to those who need it (firms, governments), and to *price* that capital continuously. Everything below is plumbing serving those two functions.

## Capital Markets vs. Money Markets

The split is maturity. **Money markets** trade short-term debt—maturities under one year—where the goal is parking cash safely and earning a little yield: Treasury bills, commercial paper, repurchase agreements (repos), and certificates of deposit. **Capital markets** trade long-term instruments (over one year): stocks and longer-dated bonds that fund multi-year investment. As a risk analyst, the practical distinction is that money-market instruments are near-cash with minimal duration risk, while capital-market instruments carry the duration, credit, and equity risk you actually model.

## Primary vs. Secondary Markets

A **primary market** transaction is a *new* issue—the issuer sells securities for the first time and keeps the proceeds. The canonical example is an IPO (initial public offering), but corporate bond issuance and Treasury auctions are also primary. A **secondary market** is where already-issued securities change hands between investors; the issuer gets nothing. NYSE, Nasdaq, and the bond dealer network are secondary markets. The secondary market matters precisely because it makes the primary market possible: nobody buys a 10-year bond at issuance unless they believe they can sell it later. Secondary-market liquidity is priced *back into* primary issuance through lower yields.

## The Major Asset Classes and Their Scale

Rough sizes, latest authoritative data (BIS, SIFMA):

- **Fixed income / bonds** — ~$145.1 trillion outstanding globally (2024, SIFMA). Debt claims paying contractual interest; a larger pool than global public equity (though not the largest asset class overall — global real estate is bigger). Subdivided into government, corporate, municipal, and securitized (e.g., asset-backed) debt.
- **Equities** — ~$126.7 trillion global market capitalization (2024, SIFMA); the US alone is nearly half. Residual ownership claims—paid last, but with unlimited upside.
- **Derivatives** — the notional headline dwarfs everything: ~$698 trillion OTC notional outstanding at year-end 2024 (BIS/ISDA), of which interest-rate derivatives are ~$548 trillion. But *notional* overstates economic exposure massively; gross market value (closer to true risk) is a tiny fraction. Don't confuse the two.
- **FX (foreign exchange)** — measured by *turnover*, not stock: $9.6 trillion traded **per day** in April 2025 (BIS Triennial Survey), up 28% from 2022. The US dollar is on one side of 89% of all trades.
- **Commodities** — smallest of the financial-derivative asset classes: ~$2.4 trillion commodity-derivative notional outstanding (BIS, 2024), spanning energy, metals, and agriculture. The *physical* market is large but most financial exposure is via futures.

A trap for newcomers: these numbers aren't comparable units. Equity and bond figures are *stocks* (outstanding value); FX is a daily *flow*; derivatives notional is a reference amount, not money at risk.

## Exchanges vs. OTC

An **exchange** (NYSE, Nasdaq, CME) is a centralized, regulated venue with standardized contracts, a central limit order book, and a clearinghouse that guarantees settlement—so counterparty risk is mutualized and prices are transparent. **Over-the-counter (OTC)** means bilateral trading through dealer networks, customized terms, less transparency, and direct counterparty exposure. Most bonds, FX, and the bulk of derivatives trade OTC; equities mostly trade on exchanges. The 2008 crisis pushed standardized OTC derivatives toward central clearing precisely because bilateral counterparty risk proved systemic.

## Price Discovery and Liquidity—Why They Matter

**Price discovery** is the process by which the market incorporates new information into a security's price through the interaction of buy and sell orders. A market with good price discovery produces prices that reflect fundamentals; a broken one produces stale or manipulated prices. **Liquidity** is the ability to transact size quickly without moving the price much. The everyday proxy is the **bid-ask spread**—the gap between the best buy (bid) and sell (ask) quote, which is the cost of immediate execution. Tight spreads and deep order books signal liquidity; widening spreads signal it's evaporating.

For a risk analyst these are not abstractions—they are the two failure modes that hurt you. When liquidity dries up, you cannot exit at marked prices, mark-to-market values become fiction, and forced selling cascades (March 2020 Treasuries, 1998 LTCM). Price discovery and liquidity are what separate a "price" you can act on from a number on a screen.

---
**Sources:** [SIFMA 2025 Capital Markets Fact Book](https://www.sifma.org/news/blog/top-10-takeaways-from-sifmas-2025-capital-markets-fact-book) · [BIS OTC derivatives](https://www.bis.org/publ/otc_hy2411.htm) · [BIS 2025 Triennial FX Survey](https://www.bis.org/press/p250930.htm) · [Britannica: primary vs secondary](https://www.britannica.com/money/primary-vs-secondary-markets)
