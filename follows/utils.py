def format_counter(recipe_count):
    recipe_count -= 3
    if recipe_count < 1:
        return ""
    end_count = recipe_count % 10
    if end_count == 1:
        return "Еще {} рецепт...".format(recipe_count)
    elif 2 <= end_count <= 4:
        return "Еще {} рецепта...".format(recipe_count)
    elif end_count >= 5:
        return "Еще {} рецептов...".format(recipe_count)
