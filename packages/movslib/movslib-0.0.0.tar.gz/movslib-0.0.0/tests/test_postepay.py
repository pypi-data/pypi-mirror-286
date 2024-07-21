# ruff: noqa: E501

from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase
from unittest import main

from movslib.model import KV
from movslib.model import Row
from movslib.postepay import read_postepay

PATH = f'{Path(__file__).parent}/test_postepay.pdf'


class TestPostepay(TestCase):
    maxDiff = None

    def test_base(self) -> None:
        kv, rows = read_postepay(PATH)

        # kv
        self.assertEqual(
            KV(
                None,
                None,
                '',
                '533317******9706',
                'DE TULLIOVITO',
                date(2023, 8, 22),
                Decimal('829.06'),
                Decimal('829.06'),
            ),
            kv,
        )

        # rows
        self.assertEqual(
            [
                # fmt: off
                Row(
                    date(2023, 8, 19),
                    date(2023, 8, 17),
                    None,
                    Decimal('585.00'),
                    'ACCREDITO TRAMITE CARTA 17/08/2023 12.31 PAYPAL *WIBROS GMBH HAUPSTSTR. 17 DEU N. 661776',
                ),
                Row(
                    date(2023, 8, 18),
                    date(2023, 8, 14),
                    Decimal('1.74'),
                    None,
                    'PAGAMENTO PEDAGGI AUTOSTRADALI 14/08/2023 18.52 PEDAGGI AUT PEDEMONTAN ASSAGO ITA N. 665208',
                ),
                Row(
                    date(2023, 8, 17),
                    date(2023, 8, 14),
                    Decimal('3.58'),
                    None,
                    'PAGAMENTO ON LINE 14/08/2023 11.01 PAYPAL *EASYPARK 35314369001 SWE N. 668949',
                ),
                Row(
                    date(2023, 8, 8),
                    date(2023, 8, 4),
                    Decimal('24.78'),
                    None,
                    'PAGAMENTO ON LINE 04/08/2023 10.19 DELIVEROO MILANO ITA N. 652715',
                ),
                Row(
                    date(2023, 7, 20),
                    date(2023, 7, 20),
                    None,
                    Decimal('20.00'),
                    'RICARICA CARTA DA CONTO RICARICA POSTEPAY. RICARICA EFFETTUATA DA VITO DE TULLIO PER ARCIMBOLDI',
                ),
                Row(
                    date(2023, 7, 8),
                    date(2023, 7, 5),
                    Decimal('35.30'),
                    None,
                    'PAGAMENTO ON LINE 05/07/2023 16.18 AMZN MKTP IT*C48TG8T55 800-279-6620 LUX N. 658840',
                ),
                Row(
                    date(2023, 7, 6),
                    date(2023, 7, 4),
                    Decimal('585.00'),
                    None,
                    'PAGAMENTO ON LINE 04/07/2023 12.05 PAYPAL *WIBROS GMBH 35314369001 DEU N. 654350',
                ),
                Row(
                    date(2023, 7, 4),
                    date(2023, 7, 4),
                    None,
                    Decimal('800.00'),
                    'RICARICA CARTA DA CONTO RICARICA POSTEPAY. RICARICA EFFETTUATA DA VITO DE TULLIO PER REGALO ELENA',
                ),
                Row(
                    date(2023, 7, 4),
                    date(2023, 6, 30),
                    Decimal('11.78'),
                    None,
                    'PAGAMENTO ON LINE 30/06/2023 10.44 DELIVEROO MILANO ITA N. 646090',
                ),
                Row(
                    date(2023, 6, 1),
                    date(2023, 5, 30),
                    Decimal('77.50'),
                    None,
                    'PAGAMENTO ON LINE 30/05/2023 10.29 DJEJT9UV03:DE TULLIO SESTO SAN GIO ITA N. 649950',
                ),
                Row(
                    date(2023, 6, 1),
                    date(2023, 5, 29),
                    Decimal('2.20'),
                    None,
                    'PAGAMENTO ON LINE 29/05/2023 21.26 PAYPAL *AZIENDATRAS 35314369001 ITA N. 640897',
                ),
                Row(
                    date(2023, 5, 30),
                    date(2023, 5, 27),
                    Decimal('2.20'),
                    None,
                    'PAGAMENTO ON LINE 27/05/2023 05.45 PAYPAL *AZIENDATRAS 0248607607 ITA N. 631566',
                ),
                Row(
                    date(2023, 5, 16),
                    date(2023, 5, 12),
                    Decimal('36.54'),
                    None,
                    'PAGAMENTO ON LINE 12/05/2023 11.54 PAYPAL *TIQETSINTER 35314369001 NLD N. 630137',
                ),
                Row(
                    date(2023, 5, 4),
                    date(2023, 5, 2),
                    Decimal('69.99'),
                    None,
                    'PAGAMENTO ON LINE 02/05/2023 04.07 NINTENDO OF EUROPE GMB FRANKFURT DEU N. 636717',
                ),
                Row(
                    date(2023, 4, 28),
                    date(2023, 4, 27),
                    Decimal('15.00'),
                    None,
                    'ADDEBITO RICARICA TELEFONICA POSTEMOBILE RICARICA TELEFONICA DA APP',
                ),
                Row(
                    date(2023, 4, 27),
                    date(2023, 4, 24),
                    Decimal('2.20'),
                    None,
                    'PAGAMENTO ON LINE 24/04/2023 21.24 PAYPAL *AZIENDATRAS 35314369001 ITA N. 639943',
                ),
                Row(
                    date(2023, 4, 26),
                    date(2023, 4, 24),
                    Decimal('3.10'),
                    None,
                    'PAGAMENTO ONLINE PAGA CON POSTEPAY CON APP 24/04/2023 10.16 SU MYCICERO S.R.L.-SOCIO N. 637551',
                ),
                Row(
                    date(2023, 4, 24),
                    date(2023, 4, 23),
                    Decimal('3.10'),
                    None,
                    'PAGAMENTO ONLINE PAGA CON POSTEPAY CON APP 23/04/2023 14.00 SU MYCICERO S.R.L.-SOCIO N. 637449',
                ),
                Row(
                    date(2023, 4, 25),
                    date(2023, 4, 23),
                    Decimal('2.20'),
                    None,
                    'PAGAMENTO ON LINE 23/04/2023 06.36 PAYPAL *AZIENDATRAS 35314369001 ITA N. 636851',
                ),
                Row(
                    date(2023, 4, 25),
                    date(2023, 4, 22),
                    Decimal('8.99'),
                    None,
                    'PAGAMENTO ON LINE 22/04/2023 16.55 AMZN MKTP IT*AH5HI24X5 800-279-6620 LUX N. 631169',
                ),
                Row(
                    date(2023, 4, 27),
                    date(2023, 4, 22),
                    Decimal('59.90'),
                    None,
                    'PAGAMENTO ON LINE 22/04/2023 16.49 PAYPAL *WWW.IKEA.IT 35314369001 ITA N. 637620',
                ),
                Row(
                    date(2023, 4, 14),
                    date(2023, 4, 12),
                    Decimal('18.98'),
                    None,
                    'PAGAMENTO ON LINE 12/04/2023 09.48 DELIVEROO MILANO ITA N. 629034',
                ),
                Row(
                    date(2023, 4, 12),
                    date(2023, 4, 8),
                    Decimal('51.06'),
                    None,
                    'PAGAMENTO ON LINE 08/04/2023 18.02 AMZN MKTP IT*VX7BN1IH5 800-279-6620 LUX N. 629392',
                ),
                Row(
                    date(2023, 4, 4),
                    date(2023, 4, 2),
                    Decimal('7.80'),
                    None,
                    'PAGAMENTO ON LINE 02/04/2023 15.25 PAYPAL *TRENORD SRL 35314369001 ITA N. 622495',
                ),
                Row(
                    date(2023, 4, 4),
                    date(2023, 4, 1),
                    Decimal('19.99'),
                    None,
                    'PAGAMENTO ON LINE 01/04/2023 18.16 GOOGLE PAYMENT IE LTD DUBLIN IRL N. 629009',
                ),
                Row(
                    date(2023, 4, 4),
                    date(2023, 4, 1),
                    Decimal('3.99'),
                    None,
                    'PAGAMENTO ON LINE 01/04/2023 14.24 AMAZON.IT*AA8LQ9TD5 WWW.AMAZON.IT LUX N. 622898',
                ),
                Row(
                    date(2023, 4, 4),
                    date(2023, 3, 31),
                    Decimal('6.20'),
                    None,
                    'PAGAMENTO ON LINE 31/03/2023 08.40 AMAZON.IT*BV88M4DB5 WWW.AMAZON.IT LUX N. 626613',
                ),
                Row(
                    date(2023, 3, 21),
                    date(2023, 3, 18),
                    Decimal('21.80'),
                    None,
                    'PAGAMENTO ON LINE 18/03/2023 19.01 MOL*CORPORATE BENEFITS 4106123456798 ITA N. 629084',
                ),
                Row(
                    date(2023, 3, 21),
                    date(2023, 3, 18),
                    Decimal('20.40'),
                    None,
                    'PAGAMENTO ON LINE 18/03/2023 04.58 DELIVEROO MILANO ITA N. 629854',
                ),
                Row(
                    date(2023, 3, 7),
                    date(2023, 3, 4),
                    Decimal('2.20'),
                    None,
                    'PAGAMENTO ON LINE 04/03/2023 17.52 PAYPAL *AZIENDATRAS 35314369001 ITA N. 613403',
                ),
                Row(
                    date(2023, 3, 4),
                    date(2023, 3, 2),
                    Decimal('43.94'),
                    None,
                    'PAGAMENTO ON LINE 02/03/2023 11.12 DELIVEROO MILANO ITA N. 612325',
                ),
                Row(
                    date(2023, 2, 27),
                    date(2023, 2, 26),
                    Decimal('15.00'),
                    None,
                    'ADDEBITO RICARICA TELEFONICA POSTEMOBILE RICARICA TELEFONICA DA APP',
                ),
                Row(
                    date(2023, 2, 22),
                    date(2023, 2, 19),
                    Decimal('48.92'),
                    None,
                    'PAGAMENTO ON LINE 19/02/2023 10.50 AMZN MKTP IT*138SS8Q84 800-279-6620 LUX N. 618847',
                ),
                Row(
                    date(2023, 2, 11),
                    date(2023, 2, 9),
                    Decimal('50.48'),
                    None,
                    'PAGAMENTO ON LINE 09/02/2023 13.47 PAYPAL *BLOOMINGEXP 35314369001 ITA N. 615549',
                ),
                Row(
                    date(2023, 1, 24),
                    date(2023, 1, 20),
                    Decimal('29.82'),
                    None,
                    'PAGAMENTO ON LINE 20/01/2023 09.38 DELIVEROO MILANO ITA N. 604978',
                ),
                Row(
                    date(2023, 1, 20),
                    date(2023, 1, 16),
                    Decimal('60.77'),
                    None,
                    'PAGAMENTO ON LINE 16/01/2023 02.19 AMZN MKTP IT*1A33F9PL4 LUXEMBOURG LUX N. 606792',
                ),
                Row(
                    date(2022, 12, 25),
                    date(2022, 12, 24),
                    Decimal('10.00'),
                    None,
                    'ADDEBITO RICARICA TELEFONICA POSTEMOBILE RICARICA TELEFONICA DA APP',
                ),
                Row(
                    date(2022, 12, 28),
                    date(2022, 12, 24),
                    Decimal('2.00'),
                    None,
                    'PAGAMENTO ON LINE 24/12/2022 09.22 PAYPAL *AZIENDATRAS 35314369001 ITA N. 699815',
                ),
                Row(
                    date(2022, 12, 13),
                    date(2022, 12, 10),
                    Decimal('52.80'),
                    None,
                    'PAGAMENTO ON LINE 10/12/2022 15.03 PAYPAL *MASSARI 0304194310 ITA N. 694045',
                ),
                Row(
                    date(2022, 10, 26),
                    date(2022, 10, 23),
                    Decimal('77.19'),
                    None,
                    'PAGAMENTO ON LINE 23/10/2022 14.56 AMZN MKTP IT*OM7KF0V75 LUXEMBOURG LUX N. 681575',
                ),
                Row(
                    date(2022, 9, 29),
                    date(2022, 9, 27),
                    Decimal('15.00'),
                    None,
                    'RICARICA TELEFONICA PT MOBILE ON LINE DEL 27/09/2022 19:10',
                ),
                Row(
                    date(2022, 9, 27),
                    date(2022, 9, 24),
                    Decimal('0.66'),
                    None,
                    'COMMISSIONE PAGAMENTO IN VALUTA ESTERA 24/09/2022 19.02 N. 672164 - VALUTA CAD 79,04 - CAMBIO 0,7597419',
                ),
                Row(
                    date(2022, 9, 27),
                    date(2022, 9, 24),
                    Decimal('60.05'),
                    None,
                    'PAGAMENTO GOOGLE PAY POS ESERCENTE 24/09/2022 19.02 GRAND VIEW - RETAIL NIAGARA FALLS CAN N. 672164',
                ),
                Row(
                    date(2022, 9, 27),
                    date(2022, 9, 23),
                    Decimal('0.10'),
                    None,
                    'COMMISSIONE PAGAMENTO IN VALUTA ESTERA 23/09/2022 23.23 N. 677156 - VALUTA CAD 11,85 - CAMBIO 0,7594937',
                ),
                Row(
                    date(2022, 9, 27),
                    date(2022, 9, 23),
                    Decimal('9.00'),
                    None,
                    'PAGAMENTO GOOGLE PAY POS ESERCENTE 23/09/2022 23.23 CARLO?S BAKERY EXPRESS TORONTO CAN N. 677156',
                ),
                Row(
                    date(2022, 9, 24),
                    date(2022, 9, 21),
                    Decimal('0.55'),
                    None,
                    'COMMISSIONE PAGAMENTO IN VALUTA ESTERA 21/09/2022 21.10 N. 672339 - VALUTA USD 49,50 - CAMBIO 1,0135354',
                ),
                Row(
                    date(2022, 9, 24),
                    date(2022, 9, 21),
                    Decimal('50.17'),
                    None,
                    'PAGAMENTO GOOGLE PAY POS ESERCENTE 21/09/2022 21.10 ROCK SHOP NEW YORK USA N. 672339',
                ),
                Row(
                    date(2022, 9, 23),
                    date(2022, 9, 21),
                    Decimal('0.08'),
                    None,
                    'COMMISSIONE PAGAMENTO IN VALUTA ESTERA 21/09/2022 20.49 N. 679711 - VALUTA USD 7,08 - CAMBIO 1,0042373',
                ),
                Row(
                    date(2022, 9, 23),
                    date(2022, 9, 21),
                    Decimal('7.11'),
                    None,
                    'PAGAMENTO GOOGLE PAY POS ESERCENTE 21/09/2022 20.49 HCW TIMES SQUARE NEW YORK USA N. 679711',
                ),
                Row(
                    date(2022, 9, 24),
                    date(2022, 9, 21),
                    Decimal('0.08'),
                    None,
                    'COMMISSIONE PAGAMENTO IN VALUTA ESTERA 21/09/2022 20.08 N. 673473 - VALUTA USD 7,29 - CAMBIO 1,0041152',
                ),
                Row(
                    date(2022, 9, 24),
                    date(2022, 9, 21),
                    Decimal('7.32'),
                    None,
                    'PAGAMENTO GOOGLE PAY POS ESERCENTE 21/09/2022 20.08 STARBUCKS STORE 08769 NEW YORK USA N. 673473',
                ),
                Row(
                    date(2022, 9, 22),
                    date(2022, 9, 20),
                    Decimal('0.22'),
                    None,
                    'COMMISSIONE PAGAMENTO IN VALUTA ESTERA 20/09/2022 19.01 N. 675380 - VALUTA USD 19,99 - CAMBIO 1,0035018',
                ),
                Row(
                    date(2022, 9, 22),
                    date(2022, 9, 20),
                    Decimal('20.06'),
                    None,
                    'PAGAMENTO GOOGLE PAY POS ESERCENTE 20/09/2022 19.01 NINTENDO NEWYORK NEW YORK USA N. 675380',
                ),
                Row(
                    date(2022, 9, 15),
                    date(2022, 9, 12),
                    Decimal('22.99'),
                    None,
                    'PAGAMENTO ON LINE 12/09/2022 21.00 PAYPAL *NINTENDO 35314369001 ITA N. 665303',
                ),
                Row(
                    date(2022, 9, 8),
                    date(2022, 9, 8),
                    None,
                    Decimal('2000.00'),
                    'RICARICA CARTA DA CONTO RICARICA POSTEPAY. RICARICA EFFETTUATA DA VITO DE TULLIO PER AMERICA E GNUA',
                ),
                Row(
                    date(2022, 9, 10),
                    date(2022, 9, 8),
                    Decimal('1039.00'),
                    None,
                    'PAGAMENTO ON LINE 08/09/2022 11.53 APPLE.COM/IT 848-789-424 ITA N. 661366',
                ),
                Row(
                    date(2022, 7, 21),
                    date(2022, 7, 18),
                    Decimal('55.98'),
                    None,
                    'PAGAMENTO ON LINE 18/07/2022 10.47 PAYPAL *BATA 0499180004 ITA N. 652089',
                ),
                Row(
                    date(2022, 7, 22),
                    date(2022, 7, 18),
                    Decimal('24.99'),
                    None,
                    'PAGAMENTO ON LINE 18/07/2022 06.30 GOOGLE PHOTOS LONDON GBR N. 658384',
                ),
                Row(
                    date(2022, 6, 20),
                    date(2022, 6, 20),
                    None,
                    Decimal('1600.00'),
                    'RICARICA POSTEPAY DA BPOL ADDEBITO SU CONTO 2022-06-20. RICARICA EFFETTUATA DA VITO DE TULLIO PER VACANZE TERRACINA',
                ),
                Row(
                    date(2022, 6, 24),
                    date(2022, 6, 20),
                    Decimal('1569.00'),
                    None,
                    'PAGAMENTO ON LINE 20/06/2022 11.07 PAYPAL *BOOKING 645486857 NLD N. 644044',
                ),
                Row(
                    date(2022, 6, 16),
                    date(2022, 6, 14),
                    Decimal('40.71'),
                    None,
                    'PAGAMENTO ON LINE 14/06/2022 09.18 DELIVEROO MILANO ITA N. 647506',
                ),
                Row(
                    date(2022, 5, 31),
                    date(2022, 5, 27),
                    Decimal('14.43'),
                    None,
                    'PAGAMENTO ON LINE 27/05/2022 10.26 DELIVEROO MILANO ITA N. 636811',
                ),
                Row(
                    date(2022, 5, 18),
                    date(2022, 5, 18),
                    None,
                    Decimal('250.00'),
                    'RICARICA POSTEPAY DA BPOL ADDEBITO SU CONTO 2022-05-18. RICARICA EFFETTUATA DA VITO DE TULLIO PER INITIAL',
                ),
                # fmt: on
            ],
            rows,
        )


if __name__ == '__main__':
    main()
