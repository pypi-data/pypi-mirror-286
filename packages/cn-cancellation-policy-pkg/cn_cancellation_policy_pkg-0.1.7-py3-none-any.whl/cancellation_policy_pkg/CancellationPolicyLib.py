from datetime import datetime, timedelta, timezone
# import pytz
from typing import List, Dict, Any, Optional
import json
import os
import pytz
import sys


class CancellationPolicy:
    def __init__(self, check_in_date: str, countryname: str = None):
        countryname = countryname.title() if countryname else None
        current_datetime_utc = datetime.now(timezone.utc)
        self.current_datetime = current_datetime_utc
        self.current_datetime = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.free_cancellation_policy = None
        self.check_in_date = check_in_date + "T23:00:00"
        self.partner_cp = []
        self.cn_polices = []
        self.country_timezone_min = None
        self.country_timezone_hour = 0
        self.all_timezones = {
            "UTC": "UTC",
            "UTC+04:30": "+4:30",
            "UTC+01:00": "+1",
            "UTC−04:00": "-4",
            "UTC−03:00": "-3",
            "UTC+04:00": "+4",
            "UTC+05:00": "+5",
            "UTC−05:00": "-5",
            "UTC+03:00": "-3",
            "UTC+06:00": "-6",
            "UTC−06:00": "-6",
            "UTC+02:00": "+2",
            "UTC+08:00": "+8",
            "UTC+07:00": "+7",
            "UTC−08:00": "-8",
            "UTC−01:00": "-1",
            "UTC+12:00": "+12",
            "UTC−10:00": "-10",
            "UTC+05:30": "+5:30",
            "UTC+03:30": "+3:30",
            "UTC+09:00": "+9",
            "UTC+10:00": "+10",
            "UTC+05:45": "+5",
            "UTC−11:00": "-11",
            "UTC+13:00": "+13",
            "UTC+11:00": "+11",
            "UTC+04": "+4",
            "UTC−12:00": "-12",
            "UTC−04:30": "-4:30"
        }

        # List of possible input date formats
        self.possible_date_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%m-%d-%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M",
            "%Y-%m-%dT%H:%M:%SZ",
            "%m/%d/%Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%y-%m-%d",
            "%d-%m-%y",
            "%Y-%m-%dT%H:%M:%S",
        ]
        self.get_country_timezone(countryname)

    def get_country_timezone(self, countryname):
        if not countryname:
            return None
        try:
            current_dir = os.path.dirname(__file__)
            file_path = os.path.join(current_dir, 'country_list.json')
            # Load the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            for item in data:
                if countryname in item:
                    country_timezone = item[countryname].get('timezones', [])
                    if country_timezone == 'UTC':
                        self.country_timezone_hour = 0
                        self.country_timezone_min = 0
                        return True
                    if country_timezone:
                        # Join the list of timezones into a single string
                        country_time = self.all_timezones.get(country_timezone)
                        if len(country_time) > 3:
                            hours, minutes = country_time.split(':')
                            self.country_timezone_hour = hours
                            self.country_timezone_min = minutes

                        else:
                            self.country_timezone_hour = country_time

        except FileNotFoundError:
            print("The country_list.json file was not found.")
        except json.JSONDecodeError:
            print("Error decoding the JSON file.")

        return None

    def convert_listing_timezone(self, chag_datetime):
        # datetime that needs to convert
        #  if datetime is UTC then no need to convert
        naive_datetime = datetime.strptime(chag_datetime, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        if int(self.country_timezone_hour) == 0:
            target_offset = timezone(timedelta(hours=0))
            target_timezone = naive_datetime.astimezone(target_offset)
            target_timezone = target_timezone + timedelta(hours=0.5)
            convert_time = target_timezone.strftime('%Y-%m-%d %H:%M:%S')
            return convert_time

        # if timezone is diffrent Convert into target timezone
        if self.country_timezone_min is not None:
            if self.country_timezone_hour > 0:
                target_offset = timezone(timedelta(hours=self.country_timezone_hour, minutes=30))
            else:
                target_offset = timezone(timedelta(hours=self.country_timezone_hour, minutes=-30))
        else:
            self.country_timezone_hour = int(self.country_timezone_hour)
            target_offset = timezone(timedelta(hours=self.country_timezone_hour))
        target_timezone = naive_datetime.astimezone(target_offset)
        target_timezone = target_timezone + timedelta(hours=0.5)
        convert_time = target_timezone.strftime('%Y-%m-%d %H:%M:%S')
        return convert_time

    def convert_dida_listing_timezone(self, chag_datetime):
        # datetime that needs to convert
        #  if datetime is UTC then no need to convert
        beijing_offset = timezone(timedelta(hours=8))
        naive_datetime = datetime.strptime(chag_datetime, '%Y-%m-%d %H:%M:%S')
        naive_datetime = naive_datetime.replace(tzinfo=beijing_offset)
        if int(self.country_timezone_hour) == 0:
            target_offset = timezone(timedelta(hours=0))
            target_timezone = naive_datetime.astimezone(target_offset)
            target_timezone = target_timezone + timedelta(hours=0.5)
            convert_time = target_timezone.strftime('%Y-%m-%d %H:%M:%S')
            return convert_time

        # if timezone is diffrent Convert into target timezone
        if self.country_timezone_min is not None:
            if self.country_timezone_hour > 0:
                target_offset = timezone(timedelta(hours=self.country_timezone_hour, minutes=30))
            else:
                target_offset = timezone(timedelta(hours=self.country_timezone_hour, minutes=-30))
        else:
            self.country_timezone_hour = int(self.country_timezone_hour)
            target_offset = timezone(timedelta(hours=self.country_timezone_hour))
        target_timezone = naive_datetime.astimezone(target_offset)
        target_timezone = target_timezone + timedelta(hours=0.5)
        convert_time = target_timezone.strftime('%Y-%m-%d %H:%M:%S')
        return convert_time

    def date_format_in_obj(self, date_str):
        for fmt in self.possible_date_formats:
            try:
                # Parse date_str into datetime object
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        # If no formats match, return the original string or raise an error
        raise ValueError(f"Date format for {date_str} not recognized")

    def format_date(self, date_str: str) -> str:
        if date_str is None:
            return self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        for fmt in self.possible_date_formats:
            try:
                # Parse date_str into datetime object
                dt = datetime.strptime(date_str, fmt)
                # Format datetime object into desired format
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
        # If no formats match, return the original string or raise an error
        raise ValueError(f"Date format for {date_str} not recognized")

    def get_check_in_date(self) -> str:
        return self.check_in_date

    def check_deadline_format(self, deadline):
        formats = ["%m/%d/%Y %H:%M", "%m/%d/%Y", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S:%A", "%Y-%m-%dT%H:%M:%SZ"]
        for fmt in formats:
            try:
                datetime.strptime(deadline, fmt)
                return fmt
            except ValueError:
                continue
        return "Unknown format"

    def round_time(self, time_str):
        # Parse the time string into a datetime object
        dt = datetime.strptime(time_str, '%I:%M %p')

        # Round the time to the nearest half-hour
        rounded_minute = (dt.minute // 30) * 30
        rounded_dt = dt.replace(minute=rounded_minute, second=0, microsecond=0)

        # If rounding up would exceed current time, round down instead
        if rounded_dt > dt:
            rounded_dt -= timedelta(minutes=30)
        return rounded_dt.strftime('%I:%M %p')

    def parse_cancellation_policies(self, total_partner: float) -> Dict[str, Any]:
        try:
            cancellation_policies_text = []
            parsed_policies = self.partner_cp
            free_cancellation = self.free_cancellation_policy
            if self.free_cancellation_policy:
                cancellation_type = "Free Cancellation"
            else:
                cancellation_type = "Non-Refundable"

            partial_booking = False
            cp_dates_added = []
            cp_i = 0
            end_policy = False
            first_free_sts = False
            if parsed_policies and len(parsed_policies) > 0:
                for key, policy in enumerate(parsed_policies):
                    ref_amt = 100 - ((total_partner - float(policy['amount'])) / total_partner) * 100
                    ref_amt = round(ref_amt)

                    if ref_amt == 0:
                        if first_free_sts:
                            cancellation_policies_text.pop()
                        ref_amt = 100
                        free_cancellation = True
                        first_free_sts = True
                        cancellation_type = "Free Cancellation"
                    elif ref_amt == 100:
                        ref_amt = 0
                        end_policy = True
                    if ref_amt > 0:
                        partial_booking = True

                    replace_start = str(policy['start'])
                    time_start = datetime.strptime(replace_start, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                    time_start = self.round_time(time_start)
                    date_start = datetime.strptime(replace_start, '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

                    replace_end = str(policy['end'])
                    time_end = datetime.strptime(replace_end, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                    time_end = self.round_time(time_end)
                    date_end = datetime.strptime(replace_end, '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

                    start_date_str = date_start + ' ' + time_start
                    end_date_str = date_end + ' ' + time_end

                    if free_cancellation and cp_i == 0:
                        cancellation_policies_text.append(
                            f"Receive a {ref_amt}% refund for your booking if you cancel before {date_end} at {time_end}")
                    elif cp_i == 0:
                        cancellation_policies_text.append(
                            f"Receive a {ref_amt}% refund for your booking if you cancel before {date_end} at {time_end}")
                    else:
                        if ref_amt != 0:
                            cancellation_policies_text.append(
                                f"Receive a {ref_amt}% refund for your booking if you cancel between {start_date_str} and {end_date_str}")
                    cp_i += 1

                if end_policy:
                    cancellation_policies_text.append(
                        f"If you cancel your reservation after {start_date_str}, you will not receive a refund. The booking will be non-refundable.")
                else:
                    cancellation_policies_text.append(
                        f"If you cancel your reservation after {end_date_str}, you will not receive a refund. The booking will be non-refundable.")

                if not partial_booking and not free_cancellation:
                    cancellation_type = "Non-Refundable"
                    cancellation_policies_text = ["You won't be refunded if you cancel this booking"]
                elif not free_cancellation and partial_booking:
                    cancellation_type = "Partial refund"
            else:
                cancellation_type = "Non-Refundable"
                cancellation_policies_text = ["You won't be refunded if you cancel this booking"]

            self.cn_polices = {
                'type': cancellation_type,
                'text': cancellation_policies_text
            }
            return self.cn_polices
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            self.cn_polices = {
                'type': '',
                'text': ''
            }
            return self.cn_polices

    # parse ratehawk cancellation policy
    def parse_ratehawk_cancellation_policy(self, pricing: List[Dict[str, Any]], total_price: float) -> List[
        Dict[str, Any]]:
        try:
            cp = []
            first_end_date = None
            # ratehawk is providing cancellation policy in UTC timezone
            if 'cancellation_penalties' in pricing[0] and 'policies' in pricing[0]['cancellation_penalties']:
                check_in_date = self.get_check_in_date()
                i = 0
                last_date = None
                # first policy
                first_policy_date = pricing[0]['cancellation_penalties']['policies'][0]['start_at']
                if first_policy_date is not None:
                    first_policy_date = self.format_date(first_policy_date)
                    first_end_date = self.format_date(first_policy_date)
                    first_amount = int(
                        round(float(pricing[0]['cancellation_penalties']['policies'][0]['amount_show']), 0))
                    first_policy_amount = first_amount
                    first_start_date = self.current_datetime
                    first_start_date_obj = datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S")
                    first_end_at_obj = datetime.strptime(first_end_date, "%Y-%m-%d %H:%M:%S")
                    if (first_end_at_obj > first_start_date_obj):
                        # first data
                        if first_policy_amount != 0:
                            self.partner_cp.append({
                                'start': self.convert_listing_timezone(first_start_date),
                                # date format (2021-07-11 00:00:00)
                                'end': self.convert_listing_timezone(first_end_date),
                                'amount': 0,
                                'currency': 'USD'
                            })
                            if first_policy_amount == 0 and self.free_cancellation_policy is None:
                                self.free_cancellation_policy = True
                    else:
                        cancellation_policy = self.parse_cancellation_policies(total_price)
                        return cancellation_policy
                i = 0
                for policy in pricing[0]['cancellation_penalties']['policies']:
                    if i == 0:
                        if first_end_date is not None:
                            start_at = first_end_date
                        else:
                            start_at = policy.get('start_at',
                                                  datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S"))
                            if start_at is None:
                                start_at = self.current_datetime
                    else:
                        start_at = end_at
                        start_at = policy.get('start_at', datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S"))
                    end_at = policy.get('end_at', check_in_date)
                    if start_at is None and end_at is None:
                        continue
                    if (end_at is None):
                        end_at = check_in_date
                    last_date = end_at
                    i += 1
                    p_amount = int(round(float(policy['amount_show']), 0))
                    if p_amount == 0:
                        amount_rtn = 0
                    elif p_amount == total_price:
                        amount_rtn = total_price
                    else:
                        amount_rtn = total_price - p_amount
                    start_at = self.format_date(start_at)
                    end_at = self.format_date(end_at)
                    self.partner_cp.append({
                        'start': self.convert_listing_timezone(start_at),
                        'end': self.convert_listing_timezone(end_at),
                        'amount': amount_rtn,
                        'currency': pricing[0]['currency_code'] if 'currency_code' in pricing[0] else "USD"
                    })
                    free_cancellation_before = pricing[0]["cancellation_penalties"]["free_cancellation_before"]
                    if free_cancellation_before is None or free_cancellation_before == "":
                        free_cancellation_before = None
                    if policy[
                        'amount_show'] == '0.00' and free_cancellation_before is not None and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy

            # Rakuten provide in UTC timezone

    def parse_rakuten_cancellation_policy(self, room_data: Dict[str, Any], total_price: float) -> List[Dict[str, Any]]:
        try:
            #  Rakuten provide cancellation policy in UTC timezone
            cancellation_policies = []
            policy_rules = room_data['cancellation_policy']
            currency_code = room_data['room_rate_currency']
            policies = policy_rules['cancellation_policies']
            # first policy
            first_policy_date = policies[0]['date_from']
            first_end_date = self.format_date(first_policy_date)
            first_policy_amount = policies[0]['penalty_percentage']
            first_start_date = self.current_datetime
            first_start_date_obj = datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S")

            first_end_at_obj = datetime.strptime(first_end_date, "%Y-%m-%d %H:%M:%S")

            if (first_end_at_obj > first_start_date_obj):
                # first data
                if first_policy_amount != 0:
                    self.partner_cp.append({
                        'start': self.convert_listing_timezone(first_start_date),  # date format (2021-07-11 00:00:00)
                        'end': self.convert_listing_timezone(first_end_date),
                        'amount': 0,
                        'currency': room_data['room_rate_currency']
                    })
                    if first_policy_amount == 0 and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            # end policy
            for rule_data in policies:

                if 'date_from' in rule_data and rule_data['date_from']:
                    start_date = self.format_date(rule_data['date_from'])
                    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                    if start_date_obj < datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S"):
                        start_date = self.current_datetime
                else:
                    start_date = self.current_datetime
                    start_date_obj = self.current_datetime

                if 'date_to' in rule_data and rule_data['date_to']:
                    end_date = self.format_date(rule_data['date_to'])
                    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                else:
                    end_date = self.current_datetime
                    end_date_obj = self.current_datetime
                # case 1 as per rakuten cancellation_policy will regularly return a date that is already in the past (i.e. 1999-01-01T17:47:00Z) This indicates that the penalty_percentage applies from the time of booking
                if start_date_obj < datetime.strptime(self.current_datetime,
                                                      "%Y-%m-%d %H:%M:%S") and end_date_obj < datetime.strptime(
                        self.current_datetime, "%Y-%m-%d %H:%M:%S"):
                    continue
                if start_date_obj > datetime.strptime(self.current_datetime,
                                                      "%Y-%m-%d %H:%M:%S") and end_date_obj <= datetime.strptime(
                        self.current_datetime, "%Y-%m-%d %H:%M:%S"):
                    end_date = self.format_date(self.get_check_in_date())

                room_price = total_price
                if rule_data['penalty_percentage'] == 0:
                    percentage = 0
                elif rule_data['penalty_percentage'] == 100:
                    percentage = 100
                else:
                    percentage = 100 - rule_data['penalty_percentage']
                amount_percentage = room_price / 100
                percentage_amount = int(round(amount_percentage * percentage))
                self.partner_cp.append({
                    'start': self.convert_listing_timezone(start_date),
                    'end': self.convert_listing_timezone(end_date),
                    'amount': percentage_amount,
                    'currency': currency_code
                })
                if rule_data['penalty_percentage'] == 0 and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy

    # please be kindly note all the cancelation are based on Beijing time
    def parse_dida_cancellation_policy(self, pricing: Dict[str, Any], total_price: float) -> List[Dict[str, Any]]:
        try:
            #  Dida provide cancellation policy in Bejing timezone
            cp = []
            check_in_date = self.format_date(self.get_check_in_date())
            pricing["RatePlanCancellationPolicyList"] = [
                entry for entry in pricing["RatePlanCancellationPolicyList"]
                if self.date_format_in_obj(entry["FromDate"]) and self.date_format_in_obj(
                    entry["FromDate"]) >= datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S")
            ]
            print(pricing)
            if 'RatePlanCancellationPolicyList' in pricing and len(pricing['RatePlanCancellationPolicyList']) > 0:
                temp_array = []
                i = 0
                last_date = None
                # check first date
                first_policy_date = pricing["RatePlanCancellationPolicyList"][0]['FromDate']
                first_policy_amount = pricing["RatePlanCancellationPolicyList"][0]['Amount']
                first_start_date = self.format_date(self.current_datetime)
                first_end_at = self.format_date(first_policy_date)
                if (first_end_at > first_start_date):
                    # first data
                    if first_policy_amount > 0:
                        self.partner_cp.append({
                            'start': self.convert_listing_timezone(first_start_date),
                            # date format (2021-07-11 00:00:00)
                            'end': self.convert_dida_listing_timezone(first_end_at),
                            'amount': 0,
                            'currency': pricing['Currency']
                        })
                        if first_policy_amount == 0 and self.free_cancellation_policy is None:
                            self.free_cancellation_policy = True
                #  first policy end
                for k, policy in enumerate(pricing['RatePlanCancellationPolicyList']):
                    if i == 0:
                        start_at = first_end_at
                    else:
                        start_at = end_at
                    if k + 1 < len(pricing['RatePlanCancellationPolicyList']):
                        next_policy = pricing['RatePlanCancellationPolicyList'][k + 1]
                        end_at = next_policy.get('FromDate', check_in_date)
                    else:
                        end_at = check_in_date
                    end_at = self.format_date(end_at)
                    end_date_obj = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                    if end_date_obj < datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S"):
                        continue
                        # end_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    last_date = end_at
                    i += 1
                    p_amount = int(round(policy['Amount'], 0))
                    total_price = int(round(total_price))
                    if p_amount == 0:
                        amount_rtn = 0
                    elif p_amount == total_price:
                        amount_rtn = total_price
                    else:
                        amount_rtn = total_price - p_amount
                    self.partner_cp.append({
                        'start': self.convert_dida_listing_timezone(start_at),  # date format (2021-07-11 00:00:00)
                        'end': self.convert_dida_listing_timezone(end_at),
                        'amount': amount_rtn,
                        'currency': pricing['Currency']
                    })
                    if policy['Amount'] == 0 and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy

    # Hp provide in UTC timezone
    def parse_hp_cancellation_policy(self, pricing: Dict[str, Any], total_hp: float, pernight_amount: float) -> List[
        Dict[str, Any]]:
        try:
            #  HP provide cancellation policy in UTC timezone
            global free_cancellation_policy
            cancellation_policies = []
            temp_array = []
            s_end_date = None
            hp_check_in_date = self.format_date(self.check_in_date)
            nonRefundable = pricing.get('nonRefundable', None)
            if nonRefundable == True:
                cancellation_policy = self.parse_cancellation_policies(total_hp)
                return cancellation_policy
            for penalty in pricing['cancelPenalties']:
                penalty['format'] = self.check_deadline_format(penalty['deadline'])
            # Sort the cancelPenalties using the determined formats
            pricing['cancelPenalties'] = sorted(
                pricing['cancelPenalties'],
                key=lambda x: datetime.strptime(x['deadline'], x['format'])
            )
            if nonRefundable is None or nonRefundable is True:
                cancellation_policy = self.parse_cancellation_policies(total_hp)
                return cancellation_policy
            # if 'freeCancellationCutOff' in pricing and pricing['freeCancellationCutOff']:
            #     s_start_at = self.current_datetime
            #     s_end_date = self.format_date(pricing['freeCancellationCutOff'])
            #     # s_end_date = s_end_date.strftime("%Y-%m-%d %H:%M:%S")
            #     if s_end_date > self.current_datetime:

            #         self.partner_cp.append({
            #             'start': self.convert_listing_timezone(s_start_at),
            #             'end': self.convert_listing_timezone(s_end_date),
            #             'amount': 0,
            #             'currency': pricing.get('currencyCode', 'USD')
            #         })

            # else:
            # check first policy
            # first policy
            first_policy_date = pricing['cancelPenalties'][0]['deadline']
            first_policy_date = first_policy_date.replace(',', '')
            first_policy_date = self.format_date(first_policy_date)
            first_end_date = self.format_date(first_policy_date)
            price_type = pricing['cancelPenalties'][0]['type']
            if price_type == 'price':
                first_amount = pricing['cancelPenalties'][0]['amount']
            else:
                first_no_of_night = pricing['cancelPenalties'][0]['nights']
                first_amount = no_of_night * pernight_amount
            first_policy_amount = first_amount
            first_start_date = self.current_datetime
            first_start_date_obj = datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S")
            first_end_at_obj = datetime.strptime(first_end_date, "%Y-%m-%d %H:%M:%S")

            if (first_end_at_obj > first_start_date_obj):
                # first data
                if first_policy_amount != 0:
                    self.partner_cp.append({
                        'start': self.convert_listing_timezone(first_start_date),  # date format (2021-07-11 00:00:00)
                        'end': self.convert_listing_timezone(first_end_date),
                        'amount': 0,
                        'currency': 'USD'
                    })
                    if first_policy_amount == 0 and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            # end policy
            last_date = None

            # deadlines = [penalty['deadline'] for penalty in pricing['cancelPenalties']]
            # formats = [check_deadline_format(deadline) for deadline in deadlines]
            # pricing['cancelPenalties'] = sorted(pricing['cancelPenalties'], key=lambda x: datetime.strptime(x['deadline'], formats))
            cancel_penalties = pricing.get('cancelPenalties', [])

            if not cancel_penalties:
                pass
            else:
                i = 0
                for k, policy in enumerate(pricing['cancelPenalties']):
                    if policy not in temp_array and 'deadline' in policy and policy['deadline']:
                        temp_array.append(policy)
                        if i == 0:
                            start_at = first_end_date
                        else:
                            start_at = last_date
                        if k + 1 < len(pricing['cancelPenalties']):
                            next_policy = pricing['cancelPenalties'][k + 1]
                            print(next_policy)
                            end_at_str = next_policy.get('deadline', hp_check_in_date)
                            end_at_str = end_at_str.replace(',', '')
                            print(end_at_str)
                            end_at = self.format_date(end_at_str)
                        else:
                            end_at = hp_check_in_date

                        if end_at == start_at:
                            continue
                        if end_at < self.current_datetime:
                            continue
                        last_date = end_at
                        i += 1
                        price_type = policy.get('type', '')
                        if price_type == 'price':
                            amount = policy.get('price', policy.get('amount', 0))
                        else:
                            no_of_night = policy.get('nights', 1)
                            amount = no_of_night * pernight_amount
                        if isinstance(start_at, str):
                            s_check_date = datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
                        else:
                            s_check_date = datetime.strptime(start_at.strftime("%Y-%m-%d %H:%M:%S"),
                                                             "%Y-%m-%d %H:%M:%S")
                        if isinstance(end_at, str):
                            e_check_date = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                        else:
                            e_check_date = datetime.strptime(end_at.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                        if e_check_date < s_check_date:
                            continue
                        if amount == 0:
                            ret_amount = 0
                        else:
                            ret_amount = total_hp - amount if total_hp > amount else total_hp
                        if isinstance(start_at, str):
                            date_strt = self.format_date(start_at)
                        else:
                            date_strt = start_at.strftime("%Y-%m-%d %H:%M:%S")
                        if isinstance(end_at, str):
                            date_end = self.format_date(end_at)
                        else:
                            date_end = end_at.strftime("%Y-%m-%d %H:%M:%S")
                        self.partner_cp.append({
                            'start': self.convert_listing_timezone(date_strt),
                            'end': self.convert_listing_timezone(date_end),
                            'amount': ret_amount,
                            'currency': pricing.get('currencyCode', 'USD')
                        })
                if pricing.get('freeCancellation') and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True
            print(self.partner_cp)
            cancellation_policy_data = self.parse_cancellation_policies(total_hp)
            return cancellation_policy_data
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_hp)
            return cancellation_policy

    # Tbo cancellation policy method
    # please be kindly note all the cancelation are based on Beijing time
    def parse_tbo_cancellation_policy(self, pricing: Dict[str, Any], total_tbo: float) -> List[Dict[str, Any]]:
        try:
            #  TBO provide cancellation policy in UTC timezone
            global free_cancellation_policy
            cp = []
            total_tbo = int(round(total_tbo))
            check_in_date = self.format_date(self.get_check_in_date())
            # Sort the cancelPenalties using the determined formats
            pricing = sorted(pricing, key=lambda x: datetime.strptime(x['FromDate'], '%d-%m-%Y %H:%M:%S'))
            #  remove past date
            pricing = [entry for entry in pricing if
                       self.date_format_in_obj(entry["FromDate"]) and self.date_format_in_obj(
                           entry["FromDate"]) >= datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S")]
            if len(pricing) > 0:
                temp_array = []
                i = 0
                last_date = None
                # check first date
                first_policy_date = pricing[0]['FromDate']
                first_end_at = self.format_date(first_policy_date)
                first_policy_amount = int(round(pricing[0]['CancellationCharge']))
                first_start_date = self.format_date(self.current_datetime)
                first_start_date_obj = datetime.strptime(first_start_date, "%Y-%m-%d %H:%M:%S")
                first_end_at_obj = datetime.strptime(first_end_at, "%Y-%m-%d %H:%M:%S")

                if first_end_at_obj > first_start_date_obj:
                    if first_policy_amount > 0:
                        self.partner_cp.append({
                            'start': self.convert_listing_timezone(first_start_date),
                            # date format (2021-07-11 00:00:00)
                            'end': self.convert_listing_timezone(first_end_at),
                            'amount': 0,
                            'currency': 'USD'
                        })
                    if first_policy_amount == 0 and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
                # print(self.partner_cp)
                for k, policy in enumerate(pricing):
                    if i == 0:
                        start_at = first_end_at
                    else:
                        start_at = last_date
                    if k + 1 < len(pricing):
                        next_policy = pricing[k + 1]
                        end_at = next_policy.get('FromDate', check_in_date)
                    else:
                        end_at = check_in_date

                    end_at = self.format_date(end_at)
                    end_date_obj = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")

                    if end_date_obj < datetime.strptime(self.current_datetime, "%Y-%m-%d %H:%M:%S"):
                        continue
                        # end_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    last_date = end_at
                    i += 1

                    if policy['ChargeType'] == 'Fixed':
                        if int(round(policy['CancellationCharge'])) == total_tbo:
                            can_amount = total_tbo
                            continue
                        elif int(round(policy['CancellationCharge'])) == 0:
                            can_amount = 0
                        else:
                            can_amount = total_tbo - int(round(policy['CancellationCharge']))
                    else:
                        percentage = int(round(policy['CancellationCharge']))
                        percentage = int(round(percentage))
                        percentage = int(round((percentage / 100) * total_tbo))
                        if percentage == total_tbo:
                            can_amount = total_tbo
                            continue
                        elif percentage == 0:
                            can_amount = 0
                        else:
                            can_amount = total_tbo - percentage

                    self.partner_cp.append({
                        'start': self.convert_listing_timezone(start_at),  # date format (2021-07-11 00:00:00)
                        'end': self.convert_listing_timezone(end_at),
                        'amount': can_amount,
                        'currency': 'USD'
                    })
                    if can_amount == 0 and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            print(self.partner_cp)
            cancellation_policy_data = self.parse_cancellation_policies(total_tbo)
            return cancellation_policy_data
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_tbo)
            return cancellation_policy

    # this method will convert property cancellation policy according to the property timezone
    # def convert_to_timezone(self, date_str, from_tz_str, to_tz_str):
    #     try:
    #         from_tz = pytz.timezone(from_tz_str)
    #         to_tz = pytz.timezone(to_tz_str)

    #         # Parse the date string
    #         naive_datetime = datetime.strptime(date_str, '%d %b %Y %I:%M %p')
    #         # Localize to the from_tz
    #         localized_datetime = from_tz.localize(naive_datetime)
    #         # Convert to the target timezone
    #         converted_datetime = localized_datetime.astimezone(to_tz)
    #         return converted_datetime
    #     except Exception as ex:
    #         print(f"Exception : {str(ex)}")
    #         return []

