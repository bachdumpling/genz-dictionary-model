def test_calculate_combinations():
    # Simple comments for testing
    comment1 = "This is a test comment"
    comment2 = "Another test comment to check bigrams"

    # Manually calculated bigrams
    expected_bigrams_comment1 = []
    expected_bigrams_comment2 = []

    # Tokenize and clean comments
    cleaned_tokens_comment1 = [token.lower() for token in word_tokenize(comment1) if token.lower() not in stopwords
                               and token.lower() not in function_words and token.lower() not in punctuation]
    cleaned_tokens_comment2 = [token.lower() for token in word_tokenize(comment2) if token.lower() not in stopwords
                               and token.lower() not in function_words and token.lower() not in punctuation]

    # Calculate bigrams using the function
    bigram_model_test = train_bigram_model([comment1, comment2])
    actual_bigrams_comment1 = calculate_combinations(cleaned_tokens_comment1, bigram_model_test, pmi_threshold)
    actual_bigrams_comment2 = calculate_combinations(cleaned_tokens_comment2, bigram_model_test, pmi_threshold)

    # Compare the results
    assert actual_bigrams_comment1 == expected_bigrams_comment1, f"Expected: {expected_bigrams_comment1}, but got: {actual_bigrams_comment1}"
    assert actual_bigrams_comment2 == expected_bigrams_comment2, f"Expected: {expected_bigrams_comment2}, but got: {actual_bigrams_comment2}"
    print("All tests passed!")


# Run the test function
test_calculate_combinations()
