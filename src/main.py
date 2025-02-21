import flet as ft
import re

def main(page: ft.Page):
    # Define allowed characters FIRST to avoid NameError
    allowed_values = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "X"}

    # Function to handle focus change - MOVED AFTER allowed_values
    def handle_change(e, next_field):
        current_value = e.control.value
        validated_value = ""
        
        for char in current_value:
            if char.upper() in allowed_values:
                validated_value += char.upper()

        e.control.value = validated_value
        page.update()

        if validated_value:
            next_field.focus()

    # Create a container to hold the results
    results_container = ft.ListView(expand=True)  # Changed to ListView for scrollability

    # Function to handle calculation
    def onClick_cowculate(e):
        inputCards = [
            txtFld1.value.upper(),
            txtFld2.value.upper(),
            txtFld3.value.upper(),
            txtFld4.value.upper(),
            txtFld5.value.upper(),
        ]

        final_results = mainFunction(inputCards)
        results_container.controls.clear()

        if final_results:
            n = 1
            for valid in final_results:
                res = f"RANK: {n}  {valid[1]} - {valid[2]}  {valid[3]}"
                results_container.controls.append(
                    ft.Row(
                        controls=[ft.Text(res, size=16, no_wrap=False)],
                    )
                )
                n += 1
        else:
            results_container.controls.append(
                ft.Row(
                    controls=[ft.Text("No valid combinations! You lose!", size=16)],
                )
            )
            
        page.update()

    # Function to clear fields
    def onClick_clear(e):
        for field in text_fields:
            field.value = ""
        results_container.controls.clear()
        txtFld1.focus()
        page.update()

    def mainFunction(inputCards):
        player_cards, regular_cards_values, k = input_cards(inputCards)
        special_cards_combinations = special_combinations_with_replacement(k)
        player_cards_values_combinations = combine_regular_with_special_cards(regular_cards_values, special_cards_combinations)
        if not player_cards_values_combinations:
            player_cards_values_combinations.append(regular_cards_values)
        valid_combinations = []
        for player_cards_values in player_cards_values_combinations:
            valid_combinations.extend(find_combinations(player_cards, player_cards_values))

        valid_combinations_sorted = sorted(valid_combinations, key=lambda score: score[0], reverse=True)  

        return valid_combinations_sorted

    def input_cards(inputCards):
        cards_dict  = {'A': 1, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'X': 1}
        player_cards = []
        regular_cards = []
        special_cards = []
        regular_cards_values = []
        k = 0

        for card in inputCards:
            if card == '3' or card == '6':
                k += 1
                special_cards.append(card)
            else:    
                regular_cards.append(card)
                regular_cards_values.append(cards_dict[card])

        sorted_regular_cards = sorted(regular_cards, key=lambda card: cards_dict[card])
        sorted_special_cards = sorted(special_cards, key=lambda card: cards_dict[card])
        player_cards = sorted_regular_cards + sorted_special_cards
        
        return player_cards, sorted(regular_cards_values), k

    def special_combinations_with_replacement(k, current_combination=None, special_cards_combinations=None):
        if current_combination is None:
            current_combination = []
        if special_cards_combinations is None:
            special_cards_combinations = []

        special_cards = [3, 6]

        if k == 0:
            sorted_combination = sorted(current_combination)
            if sorted_combination not in special_cards_combinations:
                special_cards_combinations.append(sorted_combination)
            return 

        for card in special_cards:
            current_combination.append(card)
            special_combinations_with_replacement(k - 1, current_combination, special_cards_combinations)
            current_combination.pop()

        return special_cards_combinations
        
    def combine_regular_with_special_cards(regular_cards_values, special_cards_combinations):
        combinations = []
        if special_cards_combinations:
            for special_cards_values in special_cards_combinations:
                combination = regular_cards_values + special_cards_values
                combinations.append(combination)  

        return combinations

    def find_combinations(player_cards, player_cards_value):
        base_combination = []
        valid_combination = []
        valid_combinations = []
        n = 5
        joker = "X"
        
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    base_combination = [player_cards[i], player_cards[j], player_cards[k]]
                    base_combination_value = [player_cards_value[i], player_cards_value[j], player_cards_value[k]]

                    if sum(card_values for card_values in base_combination_value) % 10 == 0 or joker in (player_cards[i], player_cards[j], player_cards[k]):                
                        score_combination = player_cards[:]  # Make a copy of hand
                        for num in base_combination:
                            score_combination.remove(num)  # Remove base combination elements
                        
                        score_combination_value = player_cards_value[:]  # Make a copy of hand
                        for num in base_combination_value:
                            score_combination_value.remove(num)  # Remove base combination elements
                        
                        score_combination.sort
                        score_combination_value.sort

                        score_sum, score_name = calculate_score(base_combination, score_combination, score_combination_value)
                        valid_combination = []
                        valid_combination.append(score_sum)
                        valid_combination.append(base_combination)
                        valid_combination.append(score_combination)
                        valid_combination.append(score_name)
                        if not any(valid_combination == valid for valid in valid_combinations):
                            valid_combinations.append(valid_combination)

        return valid_combinations                

    def calculate_score(base_combination, score_combination, score_combination_values):
        face_cards = ('J', 'Q', 'K')
        score_sum = sum(card_values for card_values in score_combination_values)
        score_name = ""

        # Five Dukes
        if all(card in face_cards for card in base_combination) and all(card in face_cards for card in score_combination):
            score_sum = 50
            score_name = "Five Dukes"
        # Five Dukes (4 Face Cards + 1 Joker)
        elif (
            any(card == 'X' for card in score_combination) and
            all(card in face_cards for card in score_combination if card != 'X')
        ):
            score_sum = 45
            score_name = "Five Dukes*"
        # Ngau Tunku
        elif any(card == 'A' for card in score_combination) and any(card in face_cards for card in score_combination):
            score_sum = 40   
            score_name = "Ngau Tunku"
        # Ngau Tunku (with Joker)
        elif (
            any(card == 'X' for card in score_combination) and 
            any(card in face_cards or card == 'A' for card in score_combination)
        ):
            score_sum = 35
            score_name = "Ngau Tunku*)"
        # Pair
        elif score_combination[0] == score_combination[1]: 
            print(score_combination[0])
            score_sum += 10
            score_name = f"Pair of {str(score_combination[0])}s"
        # Pair (with Joker)
        elif score_combination[0] == 'X':
            score_sum = 10 + (score_combination_values[1] * 2) - 1
            score_name = f"Pair of {str(score_combination[1])}s*"
        # Regular Ngau
        else:
            score_sum = (score_sum - 1) % 10 + 1       
            score_name = f"Ngau {score_sum}"
        
        return score_sum, score_name

    # UI Setup
    page.title = "Cowculator"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Create text fields
    txtFld1 = ft.TextField(border="outline", width=60, max_length=1, autofocus=True)    
    txtFld2 = ft.TextField(border="outline", width=60, max_length=1)    
    txtFld3 = ft.TextField(border="outline", width=60, max_length=1)    
    txtFld4 = ft.TextField(border="outline", width=60, max_length=1) 
    txtFld5 = ft.TextField(border="outline", width=60, max_length=1)    
    text_fields = [txtFld1, txtFld2, txtFld3, txtFld4, txtFld5]

    # Set up focus change handlers
    txtFld1.on_change = lambda e: handle_change(e, txtFld2)
    txtFld2.on_change = lambda e: handle_change(e, txtFld3)
    txtFld3.on_change = lambda e: handle_change(e, txtFld4)
    txtFld4.on_change = lambda e: handle_change(e, txtFld5)
    txtFld5.on_change = lambda e: handle_change(e, txtFld1)

    # Build UI
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("COWCULATOR", size=48, weight="bold")], alignment="center"),
                ft.Row(text_fields, alignment="center"),
                ft.Row(
                    [
                        ft.ElevatedButton("Cow-culate!", on_click=onClick_cowculate),
                        ft.ElevatedButton("Clear", on_click=onClick_clear)
                    ],
                    alignment="center",
                    spacing=20
                ),
                ft.Column(
                    [
                        ft.Text("Valid input values:", size=14, weight="underline", no_wrap=False),
                        ft.Text("1-9=Number, T=Ten, J=Jack", size=12, no_wrap=False),
                        ft.Text("Q=Queen, K=King, A=Ace of Spade, X=Joker", size=12, no_wrap=False)
                    ],
                ),
                ft.Container(
                    content=results_container,
                    height=300,  # Fixed height for results area
                    padding=10,
                )
            ],
            spacing=20,
        )
    )

ft.app(target=main)